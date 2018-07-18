from Components import datePicker
from Components import sideEffectsForm

import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as AC

# Form for adding a treatment from 'Treatments & Outcomes' page

class AddTreatmentForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self, expectedValues=None):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.form = self.driver.find_element_by_class_name('editroll')
		self.load_questions()

		self.validate(expectedValues)
		return True

	def load_questions(self):
		self.questionConts = self.form.find_elements_by_class_name('new-ques-div')
		self.questions = []
		for container in self.questionConts:
			self.questions.append(self.load_question(container))

	def load_question(self, container):
			question = {}
			radioContainers = container.find_elements_by_class_name('radio') # Div containing input and span (option text)
			datepickerContainers = container.find_elements_by_class_name('new-datepicker')
			categories = container.find_elements_by_class_name('new-treatment-dynamic') # Only for components like sideEffects or chemo options
			# Some questions have 'categories' class that aren't complex questions.
			# Make sure they also have 'treatment-group' class
			groups = None
			if categories:
				groups = container.find_elements_by_class_name('treatment-group')
			tables = container.find_elements_by_class_name('table-striped') # Drugs Removed (Chemotherapy)
			if categories and groups:
				question = self.load_complex_question(container, categories)
			elif tables:
				question = self.load_table(tables[0])
			elif len(radioContainers) > 0: # Radio button question
				question = self.load_radio_question(radioContainers)
			elif len(datepickerContainers) > 0: # Datepicker
				question['datepicker'] = datepickerContainers[0].find_element_by_tag_name('input')

			return question

	def load_radio_question(self, radioContainers):
		# Load question info. Make sure radio option isn't a subquestion
		question = {}
		subquestion_filter = [] # Add index of any subquestion radio buttons to this list
		for i in xrange(len(radioContainers)):
			# print('loading question: ' + str(i))
			if i not in subquestion_filter:
				radioCont = radioContainers[i]
				inputs = radioCont.find_elements_by_tag_name('input')
				spans = radioCont.find_elements_by_tag_name('span')

				# Test Validation
				if len(inputs) == 0:
					print('AddTreatmentForm: radio option has no inputElements?')
				elif len(spans) == 0:
					print('AddTreatmentForm: radio option has no spanElements?')

				# Get option name.
				optionName = spans[0].text
				# Check for textarea
				try:
					textareaEl = radioCont.find_element_by_tag_name('textarea')
				except NoSuchElementException:
					textareaEl = None

				# handle any subquestions
				subquestions = None
				if len(inputs) > 1: # All inputs after 1st should be secondary questions
					for inputIndex, inputEl in enumerate(inputs):
						if inputIndex > 0:

							# Add subquestion to filter list
							subquestion_filter.append(i + inputIndex)

							# Load subquestion info
							subquestions = self.load_question(radioContainers[i])

				# Pass back dict if loaded anything besides inputElement
				# todo: handle passing back secondary questions
				if textareaEl or subquestions:
					question[optionName] = {
						'element': inputs[0],
						'textareaEl': textareaEl,
						'subquestions': subquestions,
					}
				else:
					question[optionName] = inputs[0]
		return question

	def load_complex_question(self, container, categories):
		# For questions w/ multiple sections (sideEffects, chemotherapy drugs, medications added/removed)
		question = {}
		for category in categories:
			try:
				categoryName = category.find_element_by_class_name('treatment-group').text.lower()
			except NoSuchElementException:
				categoryName = None

			radioContainers = category.find_elements_by_class_name('radio')
			options = {}
			for radioCont in radioContainers:
				label = radioCont.find_element_by_tag_name('label')
				# Will have scale if option is selected
				try:
					scaleCont = radioCont.find_element_by_class_name('severity-indv-sld')
					scale = scaleCont.find_element_by_class_name('rc-slider-handle')
					scaleVal = scale.get_attribute('aria-valuenow')
				except NoSuchElementException:
					scaleVal = None

				# Save option name (key) and inputEl (value) in options dict
				# radioCont will contain treatment scale or textarea (when visible)
				optionName = label.text.lower()
				optionInput = label.find_element_by_tag_name('input')
				options[optionName] = {
					'inputEl': optionInput,
					'container': radioCont,
				}

			if categoryName:
				question[categoryName] = options

		# Check if question has datepicker (added chemotherapy medications question)
		try:
			datepickerCont = container.find_element_by_class_name('mnth-datepicker')
			question['datepicker'] = datepickerCont
		except NoSuchElementException:
			# Complex question does not have datepicker
			pass

		return question

	def load_table(self, container):
		# Table for removed chemotherapy treatments. Other uses?
		tableInfo = {}

		# Get number of columns in table and keys for each column
		tableHeader = container.find_elements_by_tag_name('thead')[0]
		th = tableHeader.find_elements_by_tag_name('th')
		num_columns = len(th)

		# keys = [] # ['treatment', 'date stopped', 'reason stopped']
		# for headerCell in th:
		# 	keys.append(headerCell.text.lower())

		# Load data for each row
		tableBody = container.find_elements_by_tag_name('tbody')[0]
		tableCells = tableBody.find_elements_by_class_name('outcomeTbl')
		count = 0;
		for i, cell in enumerate(tableCells):
			# Initialize data for new row
			if count == 0:
				treatment = None
				dateCont = None
				reasonCont = None
			remainder = i % num_columns

			# Pull data from current cell then increment count
			if remainder == 0:
				treatment = cell.text.lower()

			elif remainder == 1:
				try:
					dateCont = cell.find_element_by_class_name('mnth-datepicker')
				except NoSuchElementException:
					print('AddTreatmentForm: Could not find datepicker cont in expected table cell')

			elif remainder == 2:
				try:
					reasonCont = cell.find_element_by_class_name('Select-control')
				except NoSuchElementException:
					print('AddTreatmentForm: Could not find reason cont in expected table cell')

			count += 1

			# Should have info for all 3 columns. Add data to tableInfo and reset count
			if count == num_columns:
				if treatment == None:
					print('Row did not find treatment')
				elif dateCont == None:
					print('Row did not have dateCont')
				elif reasonCont == None:
					print('Row did not have reason')
				else:
					count = 0
					tableInfo[treatment] = {
						'date stopped': dateCont,
						'reason stopped': reasonCont,
					}

		return tableInfo

	def validate(self, expectedValues):
		self.failures = []

		if expectedValues:
			meta = expectedValues.get('meta', None)
			if meta:
				for key, value in meta.iteritems():
					if key == 'num_questions' and value != len(self.questionConts):
						self.failures.append('AddTreatment Meta: Expected ' + str(value) + ' questions. Form has ' + str(len(self.questionConts)))

		if len(self.failures) > 0:
			for failure in self.failures:
				print(failure)
				return False
		return True

######################## Test Functions ###########################

	def add_treatment(self, treatmentInfo, formAction='save'):
		questions = treatmentInfo['questions']
		# sideEffects = treatmentInfo.get('sideEffects', None)

		lastQuestionIndex = len(questions) - 1
		# questions
		for i, question in enumerate(questions):
			print('question[' + str(i) + ']')
			qType = question['type']
			questionActions = question.get('actions', None)
			if qType == 'date':
				# Container should always be 1st (latest questions are on top of page)
				self.set_date(self.questionConts[0], question['text'])
			elif qType == 'table':
				self.set_table(question)
			else:
				options = question['options']
				if qType == 'single' and len(options) > 1:
					print('Single type question:  should not pass in more than 1 option')
					return False

				if qType == 'single' or qType == 'select-all':
					# Handle all options
					for key in options:
						self.answer_question(key, options[key])
				elif qType == 'complex':
					date = question.get('date', None)
					self.answer_complex(options, date)
				else:
					print('AddTreatmentForm: unexpected question type! ' + str(qType))

			# Handle any actions necessary for this question
			# Don't need to pass in actions for 'complex' questions. Assumes they all have continue action
			if questionActions and questionActions == 'continue':
				try:
					self.questionConts[0].find_element_by_class_name('green-hvr-bounce-to-top').click()
				except NoSuchElementException:
					print('question[' + str(i) + '] did not have continue button')

			# Reload if this isn't the last question
			if i != lastQuestionIndex:
				# Should have i+1 questions
				WDW(self.driver, 10).until(lambda x: self.load({'meta': {'num_questions': i+1}}))
		return True

	def set_date(self, dateCont, date):
		# Assumes dateCont has both month/year dropdowns in it
		picker = datePicker.DatePicker(self.driver, dateCont)
		dateSet = False
		count = 0
		while not dateSet and count < 3:
			try:
				picker.set_date(date)
				dateSet = True
			except (ElementNotVisibleException, StaleElementReferenceException, ValueError, KeyError) as e:
				time.sleep(.4)
			count += 1
		if count == 3:
			print('Failed to set date')
			return False

	def answer_question(self, optionName, optionInfo, subOptionName=None):
		comment = optionInfo.get('comment', None)
		secondaryOptions = optionInfo.get('options', None)

		# Get loaded info for given option/subOption
		try:
			loadedQuestion = self.questions[0][optionName]
		except KeyError:
			print(optionName + ' not in question options')
			print('question: ' + str(self.questions[0]))
			raise KeyError()
		if subOptionName:
			loadedQuestion = loadedQuestion['subquestions'][subOptionName]

		# Grab input element out of loadedQuestion for option/subOption
		inputEl = loadedQuestion
		optionTextarea = None
		if type(loadedQuestion) is dict:
			inputEl = loadedQuestion.get('element', None)
			optionTextarea = loadedQuestion.get('textareaEl', None)

		# Make sure option is selected
		if not inputEl.is_selected():
			inputEl.click()
			if comment or secondaryOptions:
				self.load()

		# handle comment (optional)
		if comment:
			if not optionTextarea:
				optionTextarea = self.questions[0][optionName]['textareaEl']
			optionTextarea.clear()
			optionTextarea.send_keys(optionInfo['comment'])

		# handle secondaryQuestions
		if secondaryOptions:
			for secondaryOption in secondaryOptions:
				self.answer_question(optionName, secondaryOptions[secondaryOption], secondaryOption)

	def answer_complex(self, questionOptions, date=None):
		# For questions w/ categories and suboptions: i.e SideEffects or Chemotherapy treatment options

		# Date picker is probably already focused. Need to set that before selecting options
		if date:
			self.set_date(self.questionConts[0], date)

		for categoryName, options in questionOptions.iteritems():
			loadedInfo = self.questions[0][categoryName]
			self.set_category(options, loadedInfo)

		# Assuming all complex questions have 'continue' button
		try:
			self.questionConts[0].find_element_by_class_name('green-hvr-bounce-to-top').click()
		except NoSuchElementException:
			print('Complex question did not have continue button')

	def set_category(self, categoryOptions, loadedCategory):
		# Set values in sectionInfo
		for suboption, value in categoryOptions.iteritems():
			suboption = suboption.lower()
			# Grab inputEl and make sure it's selected
			try:
				inputEl = loadedCategory[suboption]['inputEl']
			except KeyError:
				print('failed to load sideEffect named: ' + str(suboption))
			if not inputEl.is_selected():
				inputEl.click()

			# Type comment, set intensity, etc
			if type(value) is dict:
				for key, optionVal in value.iteritems():
					optionContainer = loadedCategory[suboption]['container']
					if key == 'comment':
						try:
							textarea = optionContainer.find_element_by_tag_name('textarea')
							textarea.send_keys(optionVal)
						except NoSuchElementException:
							print('could not find textarea to set comment: ' + str(optionVal))
						pass
					elif key == 'date':
						# load datepicker
						# set date
						pass
					elif key == 'intensity':
						self.set_intensity(optionContainer, optionVal)

	def set_intensity(self, container, value):
		try:
			sliderEl = container.find_element_by_class_name('rc-slider-handle')
		except NoSuchElementException:
			print('SideEffectsForm: failed to load sliderEl')
		curValue = sliderEl.get_attribute('aria-valuenow')

		# Need to change intensity value?
		if value != curValue:
			xOffset = None # Every time offset doesn't work, increase by 5 and try again
			additionalOffset = 0
			while str(curValue) != str(value) and additionalOffset < 50:
				# print('additionalOffset: ' + str(additionalOffset))
				if curValue != 1: # reset to base position
					AC(self.driver).drag_and_drop_by_offset(sliderEl, -200, 0).perform()

				# Calculate offset
				# Note: monitor and window sizes affect this.
				if xOffset != None:
					# First offset wasn't correct. Increment amount of offset
					additionalOffset += 5
				xOffset = 11*(value - 1) + additionalOffset
				AC(self.driver).drag_and_drop_by_offset(sliderEl, xOffset, 0).perform()
				curValue = sliderEl.get_attribute('aria-valuenow')

	def set_table(self, questionInfo):
		# Used for Chemotherapy drugs REMOVED question
		loadedInfo = self.questions[0]

		options = questionInfo['options']
		# Options should look something like...
		# 'dexamethasone': {
		# 	'date stopped': '03/2018',
		# 	'reason stopped': 'too much travel',
		# },
		# 'adriamycin': {
		# 	'date stopped': '03/2018',
		# 	'reason stopped': 'drug cost',
		# },
		# 'melphalan': {},
		for optionName, rowData in options.iteritems():
			treatment = optionName
			date = rowData.get('date stopped', None)
			reason = rowData.get('reason stopped', None)

			if date:
				dateCont = loadedInfo[treatment]['date stopped']
				inputEl = dateCont.find_element_by_tag_name('input')
				inputEl.click()
				self.set_date(dateCont, date)

			if reason:
				reasonCont = loadedInfo[treatment]['reason stopped']
				self.set_dropdown(reasonCont, reason)


		# Assuming all complex questions have 'continue' button
		try:
			self.questionConts[0].find_element_by_class_name('green-hvr-bounce-to-top').click()
		except NoSuchElementException:
			print('Complex question did not have continue button')

	def set_dropdown(self, container, value):
		# Figure out if you need to click 'Select-value-label' or 'Select-placeholder' element
		dropdown_preSet = False
		try:
			dropdown_value = container.find_element_by_class_name('Select-value-label')
			dropdown_placeholder = None
			dropdown_preSet = True
		except NoSuchElementException:
			dropdown_value = None
			dropdown_placeholder = container.find_element_by_class_name('Select-placeholder')

		# click it
		if dropdown_preSet:
			dropdown_value.click()
		else:
			dropdown_placeholder.click()

		# load options in dropdown
		options = {}
		try:
			menu = self.form.find_element_by_class_name('Select-menu-outer')
			divs = menu.find_elements_by_tag_name('div')
			for i, div in enumerate(divs):
				if i != 0:
					options[div.text.lower()] = divs[i]
		except NoSuchElementException:
			print('Unable to find dropdown items for first diagnosis')

		# click option
		try:
			option = options[value.lower()]
			option.click()
		except (IndexError, KeyError) as e:
			print('invalid index: ' + value)
			for option in options:
				print(option)




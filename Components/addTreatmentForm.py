from Components import datePicker
from Components import sideEffectsForm
from utilityFuncs import UtilityFunctions

import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as AC

# Form for adding a treatment from 'Treatments & Outcomes' page

class AddTreatmentForm():

	def __init__(self, driver):
		self.driver = driver
		self.util = UtilityFunctions(self.driver)

	def load(self, expectedValues=None):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.form_conts = self.driver.find_elements_by_class_name('editroll')
		if not self.form_conts:
			time.sleep(.2)
			return False
		self.form = self.form_conts[0]
		self.questionConts = self.form.find_elements_by_class_name('new-ques-div')
		self.validate(expectedValues)

		self.load_questions()
		return True

	def load_questions(self):
		self.questions = []
		self.questions.append(self.load_question(self.questionConts[0]))
		# for i, container in enumerate(self.questionConts):
		# 	print('Loading question: ' + str(i))
		# 	self.questions.append(self.load_question(container))

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
				print('loading complex question')
				question = self.load_complex_question(container, categories)
			elif tables:
				# print('loading table')
				question = self.load_table(tables[0])
			elif len(radioContainers) > 0: # Radio button question
				# print('loading radio')
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
				try: # Check for textarea
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
		print('# categories: ' + str(len(categories)))
		question = {}
		for i, category in enumerate(categories):

			# Has issues loading category name sometime.
			# Make sure it's loaded before looking for options
			loadedCategoryName = False
			count = 0
			# raw_input('starting while loop for category: ' + str(i))
			while not loadedCategoryName and count < 5:
				# raw_input('count: ' + str(count))
				try:
					categoryEl = category.find_element_by_class_name('treatment-group')
					categoryName = categoryEl.text
					print('categoryName: ' + str(categoryName))
				except NoSuchElementException:
					print('no category name')
					categoryName = None
				
				if categoryName:
					loadedCategoryName = True
					radioContainers = category.find_elements_by_class_name('radio')
					options = {}
					for radioCont in radioContainers:
						label = radioCont.find_element_by_tag_name('label')

						# Save option name (key) and inputEl (value) in options dict
						# radioCont will contain treatment scale or textarea (when visible)
						optionName = label.text
						# optionInput = label.find_element_by_tag_name('input')
						options[optionName] = {
							# 'inputEl': optionInput,
							'container': radioCont,
						}

						question[categoryName] = options
				else:
					print('no category name: ' + str(i) + ', ' + str(count))
					if count == 0:
						pass
					elif count == 1:
						pass
					elif count == 2:
						pass
					elif count == 3:
						pass
					elif count == 4:
						pass
					count += 1
					time.sleep(.2)

			if count == 5:
				raw_input('failed to load category name')
			# print('count: ' + str(count))
				# raw_input('failed to find category name')

		# Check if question has datepicker (added chemotherapy medications question)
		try:
			datepickerCont = container.find_element_by_class_name('mnth-datepicker')
			question['datepicker'] = datepickerCont
		except NoSuchElementException:
			# Complex question does not have datepicker
			pass

		return question

	def load_table(self, container):
		time.sleep(2)
		# Table for removed chemotherapy treatments. Other uses?
		tableInfo = {}

		# Get number of columns in table and keys for each column
		tableHeader = container.find_elements_by_tag_name('thead')[0]
		th = tableHeader.find_elements_by_tag_name('th')
		num_columns = len(th)
		# print('numCols: ' + str(num_columns))

		# Load data for each row
		tableBody = container.find_elements_by_tag_name('tbody')[0]
		tableCells = tableBody.find_elements_by_class_name('outcomeTbl')
		column = 1;  # Keep track of which column you're in (Should be 3 columns)
		for i, cell in enumerate(tableCells):
			# print('cell: ' + str(i))
			# Initialize data for new row
			if column == 1:
				treatment = None
				dateCont = None
				reasonCont = None
			remainder = i % num_columns
			# print('reminder: ' + str(remainder))

			# Col1: Treatment Name
			if remainder == 0: 
				treatment = cell.text

			# Col2: Date stopped
			elif remainder == 1:
				try:
					dateCont = cell.find_element_by_class_name('date-select')
				except NoSuchElementException:
					print('AddTreatmentForm: Could not find datepicker cont in expected table cell')

			# Col3 Reason stopped
			elif remainder == 2:
				try:
					reasonCont = cell.find_element_by_class_name('Select-control')
				except NoSuchElementException:
					print('AddTreatmentForm: Could not find reason cont in expected table cell')

			# Should have info for all 3 columns. Add data to tableInfo and reset count
			if column == num_columns:
				if treatment == None:
					print('Row did not find treatment')
				elif dateCont == None:
					print('Row did not have dateCont')
				elif reasonCont == None:
					print('Row did not have reason')
				else:
					column = 1
					tableInfo[treatment] = {
						'date stopped': dateCont,
						'reason stopped': reasonCont,
					}
			else:
				column += 1

		return tableInfo

	def load_popup_question(self, container):
		loaded = False
		count = 0
		categories = []
		while not loaded and count < 5:
			categories = container.find_elements_by_class_name('new-treatment-dynamic')
			if not categories:
				# Side Effects popup doesn't have other class
				categories = container.find_elements_by_class_name('col-md-6')

			if len(categories) > 0:
				print('loading popup question')
				self.popup_question = self.load_complex_question(container, categories)
				if self.popup_question:
					# Make sure it loads something useful. Sometimes load_complex_question() returns {}
					loaded = True
			count += 1
			time.sleep(.4)

		if count == 5:
			print('failed to load popup categories')
			return False
		return True

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

		lastQuestionIndex = len(questions) - 1
		# questions
		for i, question in enumerate(questions):
			print('answering question[' + str(i) + ']')
			qType = question['type']
			questionActions = question.get('actions', None)
			if qType == 'date':
				# Container should always be 1st (latest questions are on top of page)
				self.set_date(self.questionConts[0], question['text'])
			elif qType == 'input':
				self.util.set_input(self.questionConts[0], question['text'])
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
				elif qType == 'popup':
					self.load_and_answer_popup(options)
				else:
					print('AddTreatmentForm: unexpected question type! ' + str(qType))

			# Handle any actions necessary for this question
			# Don't need to pass in actions for 'complex' questions. Assumes they all have continue action
			if questionActions and questionActions == 'continue':
				try:
					continue_button = self.questionConts[0].find_element_by_class_name('green-hvr-bounce-to-top')
				except NoSuchElementException:
					print('question[' + str(i) + '] did not have continue button')
				self.util.click_el(continue_button)

			# Reload if this isn't the last question. Verify has 1 extra question container
			if i != lastQuestionIndex:
				WDW(self.driver, 10).until(lambda x: self.load({'meta': {'num_questions': i+2}}))
		return True

	def load_and_answer_popup(self, options):
		# Load then answer poup
		loadedPopup = False
		count = 0
		while not loadedPopup and count < 5:
			print('loading popup ' + str(count))
			self.form_conts = self.driver.find_elements_by_class_name('editroll')
			if len(self.form_conts) == 2:
				self.load_popup_question(self.form_conts[1])
				loadedPopup = True
			time.sleep(.2)
			count += 1

		if loadedPopup:
			self.answer_popup(options)
		else:
			raw_input('no popup?')

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
		if secondaryOptions:
			print('has secondaryOptions: ' + str(secondaryOptions))

		# Get loaded info for given option/subOption
		try:
			loadedQuestion = self.questions[0][optionName]
		except KeyError:
			print(optionName + ' not in question options')
			print('question: ' + str(self.questions[0]))
			raise KeyError()
		if subOptionName:
			try:
				loadedQuestion = loadedQuestion['subquestions'][subOptionName]
			except TypeError:
				print('subOptionName: ' + str(subOptionName))
				print('loadedQuestion: ' + str(loadedQuestion))
				raw_input('wtf?')

		# Grab input element out of loadedQuestion for option/subOption
		inputEl = loadedQuestion
		optionTextarea = None
		if type(loadedQuestion) is dict:
			inputEl = loadedQuestion.get('element', None)
			optionTextarea = loadedQuestion.get('textareaEl', None)

		# Make sure option is selected
		if not inputEl.is_selected():
			self.util.click_radio(inputEl)
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
		print('answering complex')
		# For questions w/ categories and suboptions: i.e SideEffects or Chemotherapy treatment options

		# Date picker is probably already focused. Need to set that before selecting options
		if date:
			print('setting date: ' + str(date))
			self.set_date(self.questionConts[0], date)

		for categoryName, options in questionOptions.iteritems():
			print('setting category: ' + str(categoryName))
			try:
				loadedInfo = self.questions[0][categoryName]
			except KeyError:
				print('Could not find category: ' + str(categoryName))
				raise KeyError()

			self.set_category(options, loadedInfo)

		# Assuming all complex questions have 'continue' button
		try:
			continue_button = self.questionConts[0].find_element_by_class_name('green-hvr-bounce-to-top')
		except NoSuchElementException:
			print('Complex question did not have continue button')
		self.util.click_el(continue_button)

	def answer_popup(self, questionOptions, date=None):
		# Should be same as answer complex. Just use self.popup_question instead of self.questions[0]

		# Date picker is probably already focused. Need to set that before selecting options
		if date:
			self.set_date(self.form_conts[1], date)

		for categoryName, options in questionOptions.iteritems():
			try:
				loadedInfo = self.popup_question[categoryName]
			except KeyError:
				raw_input('KeyError: loadedInfo = ' + str(self.popup_question))
				raw_input('catName: ' + str(categoryName))
			self.set_category(options, loadedInfo)

		# Assuming all popup questions have 'continue' button
		try:
			continue_button = self.form_conts[1].find_element_by_class_name('green-hvr-bounce-to-top')
		except NoSuchElementException:
			print('Popup question did not have continue button')
		self.util.click_el(continue_button)

	def set_category(self, categoryOptions, loadedCategory):
		# Set values in sectionInfo
		for suboption, value in categoryOptions.iteritems():
			suboption = suboption
			# Grab inputEl and make sure it's selected
			try:
				inputEl = loadedCategory[suboption]['container'].find_element_by_tag_name('input')
				# inputEl = loadedCategory[suboption]['inputEl']
			except KeyError:
				print('failed to load sideEffect named: ' + str(suboption))
			if not inputEl.is_selected():
				self.util.click_radio(inputEl)
				# try:
				# 	inputEl.click
				# except WebDriverException:
				# 	print('cannot click on ' + str(suboption))
				# 	raise WebDriverException('AddTreatmentForm: Failed to set category. Wrong question type?')

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
					additionalOffset += 4
				xOffset = 11*(value - 1) + additionalOffset
				AC(self.driver).drag_and_drop_by_offset(sliderEl, xOffset, 0).perform()
				curValue = sliderEl.get_attribute('aria-valuenow')

	def set_table(self, questionInfo):
		# Used for Chemotherapy drugs REMOVED question
		loadedInfo = self.questions[0]
		# raw_input('loadedInfo: ' + str(loadedInfo))

		options = questionInfo['options']
		# raw_input('options: ' + str(options))
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
			# treatment = optionName
			date = rowData.get('date stopped', None)
			reason = rowData.get('reason stopped', None)

			if date:
				try:
					dateCont = loadedInfo[optionName]['date stopped']
				except KeyError:
					print('loadedInfo: ' + str(loadedInfo))
					raise KeyError('optionName: ' + str(optionName))
				self.set_date(dateCont, date)

			if reason:
				reasonCont = loadedInfo[optionName]['reason stopped']
				self.set_dropdown(reasonCont, reason)

		# Assuming all table questions have 'continue' button
		try:
			continue_button = self.questionConts[0].find_element_by_class_name('green-hvr-bounce-to-top')
		except NoSuchElementException:
			print('Complex question did not have continue button')
		self.util.click_el(continue_button)

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
			self.util.click_el(dropdown_value)
		else:
			self.util.click_el(dropdown_placeholder)

		# load options in dropdown
		options = {}
		try:
			menu = self.form.find_element_by_class_name('Select-menu-outer')
			divs = menu.find_elements_by_tag_name('div')
			for i, div in enumerate(divs):
				if i != 0:
					options[div.text] = divs[i]
		except NoSuchElementException:
			print('Unable to find dropdown items for first diagnosis')

		# click option
		try:
			option = options[value]
			self.util.click_el(option)
		except (IndexError, KeyError) as e:
			print('invalid index: ' + value)
			for option in options:
				print(option)

	




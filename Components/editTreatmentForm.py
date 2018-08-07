from Components import datePicker
from Components import sideEffectsForm

import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as AC

# Form for adding a treatment from 'Treatments & Outcomes' page

class EditTreatmentForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self, expectedValues=None):
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.load_question_containers()
		return self.validate(expectedValues)

	def load_question_containers(self):
		self.question_containers = self.driver.find_elements_by_class_name('new-ques-div')

	def validate(self, expectedValues):
		if expectedValues:
			pass

		return True

	def validate_form(self, expectedInfo):
		failures = []

		num_questions = expectedInfo.get('num_questions', None)
		if num_questions:
			if num_questions != len(self.question_containers):
				failures.append('EditTreatmentForm: Expected ' + str(num_questions) + ' questions. Loaded ' + str(len(self.question_containers)))
			else:
				print('EditForm: correct # questions')

		if len(failures) > 0:
			for failure in failures:
				print(failure)
			raise Exception('Failed to validate EditTreatmentForm')

	def get_state(self, question):
		# Is question 'static', 'editable', or 'editing'
		state = 'static'
		editButton = None
		actionButtons = None
		try:
			# Edit question button?
			editButton = question.find_element_by_class_name('edit-module-btn')
			state = 'editable'
		except NoSuchElementException:
			# Green Action buttons? (save, cancel)
			actionButtons = question.find_elements_by_class_name('green-hvr-bounce-to-top')
			state = 'editing'

		return {'state': state, 'editButton': editButton, 'actionButtons': actionButtons}

	def open_and_edit_question(self, questionInfo):
		# Make sure question is in edit mode
		questionIndex = questionInfo['index']
		print('editing question[' + str(questionIndex) + ']')
		question = self.question_containers[questionIndex]
		questionEls = self.get_state(question)
		if questionEls['state'] == 'static':
			print('unable to change static question[' + str(questionIndex) + ']')
			return False
		elif questionEls['state'] == 'editable':
			questionEls['editButton'].click()
			# Reload questions to avoid staleException
			self.load_question_containers()
			questionCont = self.question_containers[questionIndex]

		self.edit_question(questionCont, questionInfo)

	def edit_question(self, questionCont, questionInfo):
		# Question should already be in edit mode
		options = questionInfo.get('options', None)
		date = questionInfo.get('date', None)
		complexOptions = questionInfo.get('complex', None)
		if options:
			for key in options:
				self.answer_question(key, options[key], questionCont)
			# self.set_option(options, questionCont)
		elif date:
			self.set_date(date, questionCont)
		elif complexOptions:
			self.set_complex(complexOptions, questionCont)
		# raw_input('done editing?')
		self.save_question(questionCont)

	def save_question(self, question):
		buttons = question.find_elements_by_class_name('green-hvr-bounce-to-top')
		if len(buttons) > 0:
			save_button = buttons[-1]
			save_button.click()
		else:
			raw_input('no buttons in question?')
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		# Need to reload page?

	def answer_question(self, optionName, optionInfo, questionCont):
		comment = optionInfo.get('comment', None)
		secondaryOptions = optionInfo.get('options', None)
		# raw_input('optionInfo: ' + str(optionInfo))

		# Get loaded info for given option/subOption
		try:
			loadedQuestion = self.load_question(questionCont)# self.questions[0][optionName]
			# raw_input('loadedInfo: ' + str(loadedQuestion))
			loadedOption = loadedQuestion[optionName]
			# raw_input('loadedOption: ' + str(loadedOption))
		except KeyError:
			print(optionName + ' not in question options')
			raise KeyError()
		# if subOptionName:
		# 	loadedQuestion = loadedQuestion['subquestions'][subOptionName]

		# Grab input element out of loadedQuestion for option/subOption
		inputEl = loadedOption
		optionTextarea = None
		if type(loadedOption) is dict:
			inputEl = loadedOption.get('element', None)
			optionTextarea = loadedOption.get('textareaEl', None)

		# Make sure option is selected
		if not inputEl.is_selected():
			inputEl.click()
			if comment or secondaryOptions:
				self.load()

		# handle comment (optional)
		if comment:
			optionTextarea.clear()
			optionTextarea.send_keys(comment)

		# handle secondaryQuestions
		if secondaryOptions:
			for secondaryOption in secondaryOptions:
				# raw_input('about to answer secondary question')
				self.answer_question(secondaryOption, secondaryOptions[secondaryOption], loadedOption['subquestions']['container'])

	# def set_option(self, options, questionCont):
	# 	# option might be string (optionName), or might be dictionary with extra info (subquestions, comment text)
	# 	raw_input('options: ' + str(options))
	# 	loadedQuestion = self.load_question(questionCont)
	# 	raw_input('loadedInfo: ' + str(loadedQuestion))
	# 	optionName = options
	# 	subOptions = []
	# 	comment = None
	# 	if type(options) == dict:
	# 		# {'Other': {'comment': 'Radiation treatment Y'}}

	# 		# {'I discontinued this treatment': {
	# 		# 	'options': {
	# 		# 		'Too much travel': {},
	# 		# 		'Too much time in the clinic': {},
	# 		# 	},
	# 		# }}
	# 		for name, info in options.iteritems():
	# 			optionName = name
	# 			comment = info.get('comment', None)
	# 	inputEl = loadedQuestion.get(optionName, None)
	# 	if type(inputEl) is dict:
	# 		# get inputEl if questionInfo[optionName] has extra info
	# 		inputEl = inputEl['element']
	# 	if inputEl and not inputEl.is_selected():
	# 		inputEl.click()
	# 	else:
	# 		print('Question does not have option: ' + str(options))

	# 	if comment:
	# 		textarea = questionCont.find_element_by_tag_name('textarea')
	# 		textarea.clear()
	# 		textarea.send_keys(comment)

	def load_question(self, questionCont):
		# radioCont = question.find_element_by_class_name('new-treatment-outcome-div')
		radios = questionCont.find_elements_by_class_name('radio')
		questionInfo = {}
		subquestion_filter = [] # Add index of any subquestion radio buttons to this list
		for i, radio in enumerate(radios):
			if i not in subquestion_filter: # Don't load info if current radio option is a subquestion
				inputs = radio.find_elements_by_tag_name('input')
				spans = radio.find_elements_by_tag_name('span')

				# Test Validation
				if len(inputs) == 0:
					print('EditTreatmentForm: radio option has no inputElements?')
				elif len(spans) == 0:
					print('EditTreatmentForm: radio option has no spanElements?')

				# Get option name.
				optionName = spans[0].text
				# Check for textarea
				try:
					textareaEl = radio.find_element_by_tag_name('textarea')
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
							subquestions = self.load_question(radios[i])

				# Pass back dict if loaded anything besides inputElement
				# todo: handle passing back secondary questions

				if textareaEl or subquestions:
					questionInfo[optionName] = {
						'element': inputs[0],
						'textareaEl': textareaEl,
						'subquestions': subquestions,
					}
				else:
					questionInfo[optionName] = inputs[0]
		questionInfo['container'] = questionCont
		return questionInfo

	def set_complex(self, newOptions, container):
		# For questions w/ multiple sections (sideEffects, chemotherapy drugs, medications added/removed)
		categories = container.find_elements_by_class_name('new-treatment-dynamic')
		question = {}
		for i, category in enumerate(categories):

			# Has issues loading category name sometime.
			# Make sure it's loaded before looking for options
			loadedCategoryName = False
			count = 0
			while not loadedCategoryName and count < 5:
				try:
					categoryEl = category.find_element_by_class_name('treatment-group')
					categoryName = categoryEl.text.lower()
				except NoSuchElementException:
					categoryName = None

				if categoryName:
					# print('categoryName: ' + str(categoryName))
					loadedCategoryName = True

					# Does newOptions have any in this category?
					changesToCategory = False
					newCategoryOptions = newOptions.get(categoryName, None)
					if newCategoryOptions:
						changesToCategory = True

					radioContainers = category.find_elements_by_class_name('radio')
					options = {}
					for radioCont in radioContainers:
						label = radioCont.find_element_by_tag_name('label')


						# Save option name (key) and inputEl (value) in options dict
						# radioCont will contain treatment scale or textarea (when visible)
						optionName = label.text.lower()
						optionInput = label.find_element_by_tag_name('input')

						if not changesToCategory:
							# Make sure every option in category is de-selected
							if optionInput.is_selected():
								optionInput.click()
						else:
							# Check if this option needs to be selected
							newOption = newCategoryOptions.get(optionName, '')
							# Should be {} (has option) or {'intensity': x} (has option and need to set intensity)
							if newOption != '':
								# Has this option. Select it and set intensity (if applicable)
								if not optionInput.is_selected():
									optionInput.click()

								# Handle setting sideEffects
								if newOption.get('intensity', None):
									hasIntensity = False

									self.set_intensity(radioCont, newOption['intensity'])
							else:
								# Doesn't have option. Make sure it's not selected
								if optionInput.is_selected():
									optionInput.click()

				else:
					count += 1
					time.sleep(.2)
					# raw_input('failed to find category name: ' + str(count))

			# print('count: ' + str(count))
				# raw_input('failed to find category name')

		# Check if question has datepicker (added chemotherapy medications question)
		try:
			datepickerCont = container.find_element_by_class_name('mnth-datepicker')
			question['datepicker'] = datepickerCont
		except NoSuchElementException:
			# Complex question does not have datepicker
			pass

	def set_date(self, date, question):
		picker = datePicker.DatePicker(self.driver, question.find_element_by_class_name('new-datepicker'))
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

	def leave_form(self):
		buttons = self.driver.find_elements_by_class_name('green-hvr-bounce-to-top')
		back_button = buttons[1]
		back_button.click()
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def edit_treatment(self, newTreatmentInfo):
		for i, info in enumerate(newTreatmentInfo):
			if i == 0: # 1st item should have validation info for whole form
				self.validate_form(info)
			else: # Items after 1st should be questions
				self.open_and_edit_question(info)
		self.leave_form()
		return True


######################## Treatment Metadata ############################

# Chemotherapy
		# 0: Treatment Type [0]
		# 1: Start Date [1]
		# 2: Currently taking? [2]
		# 3: End Date NA/[3]
		# 4: Maintenance therapy? [3]/[4]
		# 5: Type of chemo [4]/[5]
		# 6: Changes? [5]/[6]
			# 7: Added NA/[6]/[7]
			# 8: Removed NA/6,7,8
		# 7: Best response -2
		# 8: Side Effects -1

# Clinical
		# 0: Treatment Type [0]
		# 1: Start Date [2]
		# 2: Currently taking? [3]
		# 3: End Date NA/[4]
		# 4: NCT # [1]
		# 5: Main treatment [4]/[5]
		# 6: Best response -2
		# 7: Side Effects -1


# Extra (Bone strengtheners, Antibiotics, Antifungal)
	# Bone strengthener (edit)
		# 0: Treatment Type [0]
		# 1: Bone Strengthener Type [2]
		# 2: Start Date [3]
		# 3: Are you currently taking bone strengtheners? [4]
		# 4: End Date [5]/NA
		# 5. Frequency [5]/[6] (-1)

	# Antibiotics (edit)
		# 0: Treatment Type [0]
		# 1: Antibiotics Type [2]
		# 2: Start Date [3]
		# 3: Currently taking antibiotics? [4]
		# 4: End Date [5]/NA

	# Antifungal (edit)
		# 0: Treatment Type [0]
		# 1: Antifungal Type [2]
		# 2: Start Date [3]
		# 3: Currently taking antifungal? [4]
		# 4: End Date [5]/NA


# Radiation
		# 0: Treatment Type [0]
		# 1: Radiation type [1]
		# 2: Start Date [2]
		# 3: End Date [3]
		# 4: Best response -2
		# 5: Side Effects -1


# Stemcell (non induction)
		# 0: Treatment Type [0]
		# 1: Stemcell type [1]
		# 2: SC Start Date [3] [9] if is induction therapy (+6)
		# 3: Type of chemo [4] ('Melphalan (Alkeran)' unless q[4] was answered w/ comment)
			# 4: Dose of chemo drug (q[4] subquestion #2)
		# 5: Best response -3
		# 6: Side Effects -2

# Induction
		# 0: Treatment Type ('induction therapy')
		# 1: Induction Start Date [3]
		# 2: Still taking? [4]
		# 3: Induction end date N/A/[5]
		# 4: Type of induction therapy [5]/[6]
		# 5: Induction changes? [6]/[7]
		# 6: Induction Best response [7]/[8]
		# 7: Induction Side Effects [8]/[9]


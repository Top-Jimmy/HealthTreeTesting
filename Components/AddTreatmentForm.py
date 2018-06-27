from Components import datePicker
from Components import sideEffectsForm

import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Form for adding a treatment from 'Treatments & Outcomes' page

class AddTreatmentForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self, expectedValues=None):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.form = self.driver.find_element_by_class_name('editroll')
		self.questionConts = self.form.find_elements_by_class_name('new-ques-div')
		self.load_questions()

		# self.validate(expectedValues)
		return True

	def load_questions(self):
		self.questions = []
		for container in self.questionConts:
			self.questions.append(self.load_question(container))

	def load_question(self, container):
			question = {}
			radioContainers = container.find_elements_by_class_name('radio') # Div containing input and span (text)
			datepickerContainers = container.find_elements_by_class_name('new-datepicker')
			if len(radioContainers) > 0: # Radio button question

				# Load question info. Make sure radio option isn't a subquestion
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
			elif len(datepickerContainers) > 0: # Datepicker
				question['datepicker'] = datepickerContainers[0].find_element_by_tag_name('input')

			return question

	# def validate(self, expectedValues):
	# 	failures = []
	# 	if expectedValues:
	# 		if expectedValues['walk_sixhours'] == 'no' and not self.walk_sixhoursno_radio.get_attribute('checked'):
	# 			failure.append('FitLvlForm: Expecting "no" to walking six or more hours a week')
	#

		# if len(failures) > 0:
		# 	for failure in failures:
		# 		print(failure)
		# 	raise NoSuchElementException('Failed to load AddTreatmentForm')

	# def read_warning(self):
	# 	inputs = ['username', 'email', 'password', 'confirm password']
	# 	warnings = []
	# 	warning_els = [
	# 		self.username_warning, self.email_warning, self.password_warning, self.confirm_password_warning,
	# 	]
	# 	for i, warning_el in enumerate(warning_els):
	# 		text = warning_el.text
	# 		if len(text) > 0:
	# 			warnings.append({
	# 				'inputName': inputs[i],
	# 				'text': text,
	# 			})
	# 	if len(warnings) > 0:
	# 		return warnings
	# 	return None

	# def interpret_warning(self, warningText):
	# 	warningType = 'undefined'
	# 	warningMsg = ''
	# 	if warningText == 'Please enter a valid email address.':
	# 		warningType = 'Invalid credentials'
	# 		warningMsg = 'forgotPwForm: Submit form warning'

	# 	return {
	# 		'msg', warningMsg,
	# 		'text', warningText,
	# 		'type', warningType,
	# 	}

	def add_treatment(self, treatmentInfo):
		questions = treatmentInfo['questions']
		sideEffects = treatmentInfo.get('sideEffects', None)

		# questions
		for i, question in enumerate(questions):
			loadedIndex = -(i+1) # Questions are loaded in opposite order
			# loadedQuestion = self.questions[loadedIndex]
			qType = question['type']
			if qType == 'date':
				# Assuming datepicker already selected and visible
				picker = datePicker.DatePicker(self.driver)
				dateSet = False
				while not dateSet:
					try:
						picker.set_date(question['text'])
						dateSet = True
					except (ElementNotVisibleException, StaleElementReferenceException, ValueError, KeyError) as e:
						print('Failed to set date. Page probably reloaded')
						time.sleep(.4)
			elif qType == 'single' or qType == 'select-all':
				options = question['options']
				actions = question.get('actions', None)
				if qType == 'single' and len(options) > 1:
					print('Single type question:  should not pass in more than 1 option')
					return False

				# Handle all options
				for key in options:
					self.answer_question(key, options[key], loadedIndex)

				if actions and actions == 'continue':
					self.questionConts[loadedIndex].find_element_by_class_name('green-hvr-bounce-to-top').click()

			self.load()

		# side effects
		if sideEffects:
			# load sideEffectForm
			effectsForm = sideEffectsForm.SideEffectsForm(self.driver)
			WDW(self.driver, 10).until(lambda x: effectsForm.load())
			effectsForm.set(sideEffects)
			raw_input('?')


	def answer_question(self, optionName, optionInfo, loadedIndex, subOptionName=None):
		comment = optionInfo.get('comment', None)
		secondaryOptions = optionInfo.get('options', None)

		# Get loaded info for given option/subOption
		loadedQuestion = self.questions[loadedIndex][optionName]
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
				optionTextarea = self.questions[loadedIndex][optionName]['textareaEl']
			optionTextarea.clear()
			optionTextarea.send_keys(optionInfo['comment'])

		# handle secondaryQuestions
		if secondaryOptions:
			for secondaryOption in secondaryOptions:
				self.answer_question(optionName, secondaryOptions[secondaryOption], loadedIndex, secondaryOption)



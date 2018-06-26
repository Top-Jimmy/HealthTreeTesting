import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class CurrentHealthForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		self.question_elements = self.form.find_elements_by_class_name('custom-current-health')
		self.questions = []
		for i, question in enumerate(self.question_elements):
			self.load_question(self.question_elements[i])

		self.continue_button = self.form.find_element_by_class_name('submitForm')
		# raw_input(self.questions)
		self.validate(expectedValues)
		return True

	def load_question(self, container):
		# Load question title (label), value, and any secondary questions and their values
		labels = container.find_elements_by_tag_name('label')
		question_label = labels[0].text
		value = None
		secondaryQuestions = []

		# Value: None if not set
		options = ['yes', 'no', 'dont know']
		for i, label in enumerate(labels):
			if i > 0 and i < 4:
				classes = label.get_attribute('class')
				if 'active' in classes:
				 	value = options[i - 1]
		# Find secondary questions
		if value == 'yes':
			secondary_container = container.find_element_by_class_name('custom-history_label')
			secondary_questions = container.find_elements_by_class_name('form-check')

			for secondary_question in secondary_questions:
				secondary_label = secondary_question.text
				secondary_input = secondary_question.find_element_by_tag_name('input')

				selected = secondary_input.is_selected()

				secondaryQuestions.append({secondary_label: selected})

		question = {
			'name': question_label,												# name: Kidney Conditions
			'value': value,																# value: 'yes'
			'secondaryQuestions': secondaryQuestions, 		# secondaryQuesitons: [
		} 																								# {'Mild kidney problems (renal impairment)': False},
		self.questions.append(question)										# {'Severe kidney problems or on dialysis': False},]

	def validate(self, expectedValues):
		failures = []
		if expectedValues:

			# meta validation
			try:
				meta_validators = expectedValues['meta']
				for validator in meta_validators:
					for key, value in validator.iteritems():
						if key == 'num_questions' and value != len(self.questions):
							failures.append('CurrentHealthForm Meta: Expected ' + str(value) + ' questions. Form has ' + str(len(self.questions)))
			except KeyError:
				# No meta validation
				pass

			# Form validation
			# expectedValues should be dictionary containing {'questions': []}
			expectedQuestions = None
			try:
				expectedQuestions = expectedValues['questions']
			except KeyError:
				# No form validation
				pass
			if expectedQuestions:
				# Check # of questions match
				if len(expectedQuestions) != len(self.questions):
					failures.append('CurrentHealthForm: Expecting ' + str(len(expectedQuestions)) + ' questions. Loaded '
						+ str(len(self.questions)))
				else:
					# Each key in each expectedQuestion (secondaryQuestions, name, value) should exist in loadedQuestion and match it's value
					for i, expectedQuestion in enumerate(expectedQuestions):
						loadedQuestion = self.questions[i]
						# print('comparing ' + str(i) + ': ' + str(expectedQuestion))
						# print('with ' + str(loadedQuestion))
						# raw_input('?')
						for key, expectedValue in expectedQuestion.iteritems():
							try:
								if loadedQuestion[key] != expectedValue:
									failures.append('CurrentHealthForm: Question ' + str(i) + ' expected value "'
										+ expectedValue + '". Loaded "' + loadedQuestion[key] + '"')
							except (TypeError, KeyError) as e:
								# raw_input(str(self.questions[i]))
								failures.append('CurrentHealthForm: Expected Key "' + key + '". Not found in question ' + str(i))

		if len(failures) > 0:
			for failure in failures:
				print(failure)
			raise NoSuchElementException('Failed to load CurrentHealthForm')

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

	def submit(self, questionInfo, action):
		try:
			questionInfo = questionInfo['questions']
		except KeyError:
			pass

		results = []
		for i, question in enumerate(questionInfo):
			print('answering question: ' + str(i))
			results.append(self.answer_question(i, question))

		if action == 'submit':
			self.continue_button.click()
		return True

	def answer_question(self, index, questionInfo):
		container = self.question_elements[index]
		labels = container.find_elements_by_tag_name('label')
		question_label = labels[0].text
		labelIndex = {'yes': 1, 'no': 2, 'dont know': 3}

		# If right question, set value
		if question_label == questionInfo['name']:
			i = labelIndex[questionInfo['value']]
			labels[i].click()

			# Handle setting any secondary questions
			if questionInfo['value'] == 'yes' and questionInfo['secondaryQuestions']:
				expectedSecondaryInfo = questionInfo['secondaryQuestions']
				secondary_container = container.find_element_by_class_name('custom-history_label')
				secondary_questions = container.find_elements_by_class_name('form-check')

				# Check # of secondary questions
				if len(secondary_questions) != len(questionInfo['secondaryQuestions']):
					print('CurrentHealth question "' + str(index) + '" expects ' + str(len(questionInfo['secondaryQuestions']))
						+ '. Loaded ' + str(len(secondary_questions)))
					return False

				# Set value for each secondary question
				for i, question in enumerate(secondary_questions):
					question_name = question.text
					input_el = question.find_element_by_tag_name('input')

					if input_el.is_selected() != expectedSecondaryInfo[i][question_name]:
						input_el.click()
					# else:
					# 	print(str(index) + ' already has correct value')

		else:
			print('Index "' + str(index) + '": Expecting ' + question_label + ' to equal ' + questionInfo['name'])
			return False
		return True







import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

# Form for adding a treatment from 'Treatments & Outcomes' page

class AddTreatmentForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self, expectedValues=None):
		self.form = self.driver.find_element_by_class_name('editroll')
		self.questionConts = self.form.find_elements_by_class_name('new-ques-div')
		self.load_questions()

		# self.validate(expectedValues)
		return True

	def load_questions(self):
		# Loop through questions. Capture key (option text) and value (is selected) and store in self.questions
		self.questions = []
		for container in self.questionConts:
			question = []
			radios = container.find_elements_by_class_name('radio') # Div containing input and span (text)
			for radio in radios:
				value = radio.find_element_by_tag_name('input').is_selected()
				key = radio.text
				question.append({
					key: value,
				})
			self.questions.append(question)


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
		questionInfo = treatmentInfo['questions']
		for question in questionInfo:
			# Set values from question for each radio button

	# def set_question(self, questionIndex, value):
	# 	row = self.rows[questionIndex]

	# 	labels = row.find_elements_by_tag_name('label')
	# 	if value == True:
	# 		labels[1].click()
	# 	else:
	# 		labels[2].click()

	# def submit(self, fitnessInfo):
	# 	for i, value in enumerate(fitnessInfo):
	# 		self.set_question(i, value)
	# 		time.sleep(.4)
	# 		self.load()

	# 	return True

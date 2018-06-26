import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class FitLvlForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues=None):
		self.form = self.driver.find_element_by_class_name('mui-form')
		self.rows = self.form.find_elements_by_class_name('fitness-form-group')

		self.questions = []
		for row in self.rows:
			labels = row.find_elements_by_tag_name('label')
			value = None
			for i, label in enumerate(labels):
				if i != 0:
					classes = label.get_attribute('class')
					if 'active' in classes:
						if i == 1:
							value = True
						elif i == 2:
							value = False
			self.questions.append(value)

		self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []

		# Should be at least 1 question
		if len(self.questions) == 0:
			failures.append('FivLvlForm: No questions loaded')

		if len(failures) > 0:
			for failure in failures:
				print(failure)
			raise NoSuchElementException('Failed to load FivLvlForm')

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

	def set_question(self, questionIndex, value):
		# row = self.rows[questionIndex]
		if value != self.questions[questionIndex]:

			# last 2 labels are option selectors
			labels = self.rows[questionIndex].find_elements_by_tag_name('label')
			for i, row in enumerate(self.rows):
				if i != 0:
					if value:
						labels[1].click()
					else:
						labels[2].click()

	def submit(self, fitnessInfo):
		for i, value in enumerate(fitnessInfo):
			print(str(i))
			self.set_question(i, value)
			time.sleep(.4)
			# Validate on the last question
			if (i + 1) < len(fitnessInfo):
				self.load()
			else:
				self.load(fitnessInfo)
		return True

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class FeedbackForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_element_by_class_name('editroll')
		buttons = self.form.find_elements_by_tag_name('button')

		self.feedback_input = self.form.find_element_by_tag_name('textarea')
		self.submit_button = self.buttons[0]
		self.cancel_button = self.buttons[1]
		self.validate()
		return True

	def validate(self):
		failures = []
		if self.feedback_input.get_attribute('placeholder') != 'Your highly valuable feedback goes here...':
			failures.append('FeedbackForm: Unexpected textarea placeholder')
		if self.submit_button.text != 'Submit':
			failures.append('FeedbackForm: Unexpected submit button text: ' + self.submit_button.text)
		if self.cancel_button.text != 'Cancel':
			failures.append('FeedbackForm: Unexpected cancel button text ' + self.cancel_button.text)
		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load FeedbackForm')

	# def read_warning(self):
	# 	inputs = ['Sign In', 'Password']
	# 	warnings = []
	# 	for i, warning_el in enumerate([self.login_warning, self.password_warning]):
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
	# 	if warningText == 'Please enter a valid email address.':
	# 		warningType = 'invalid credentials'
	# 	elif warningText == 'Please enter username.':
	# 		warningType = 'missing username'
	# 	elif warningText == 'Please enter password.':
	# 		warningType = 'missing password'

	# 	return {
	# 		'msg': 'forgotPwForm: Submit form warning. ' + warningMsg,
	# 		'text': warningText,
	# 		'type': warningType,
	# 	}

	def submit(self, feedback, action='submit'):
		if feedback:
			self.feedback_input.clear()
			self.feedback_input.send_keys(feedback)
		if action == 'submit':
			self.submit_button.click()
		else:
			self.cancel_button.click()
		return True


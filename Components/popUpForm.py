from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class PopUpForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.container = self.driver.find_element_by_class_name('react-confirm-alert')
		buttons = self.container.find_elements_by_tag_name('button')

		self.confirm_button = self.buttons[0]
		self.cancel_button = self.buttons[1]
		self.validate()
		return True

	def validate(self):
		failures = []
		if self.confirm_button.text != 'Confirm':
			failures.append('PopUpForm: Unexpected confirm button text: ' + self.confirm_button.text)
		if self.cancel_button.text != 'Cancel':
			failures.append('PopUpForm: Unexpected cancel button text ' + self.cancel_button.text)
		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load PopUpForm')

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

	def confirm(self, action='submit'):
		if action == 'submit':
			self.confirm_button.click()
		else:
			self.cancel_button.click()
		return True


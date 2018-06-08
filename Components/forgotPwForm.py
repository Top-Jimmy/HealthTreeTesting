import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class ForgotPwForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_element_by_tag_name('form')
		anchors = self.form.find_elements_by_tag_name('a')

		self.email_input = self.form.find_element_by_id('email')
		self.email_warning = self.form.find_element_by_tag_name('small')

		self.submit_button = self.form.find_element_by_tag_name('button')

		self.load_validation()
		return True

	def load_validation(self):
		failures = []
		if self.submit_button.text != 'Submit':
			failures.append('forgotPasswordForm1: Expecting "Submit", got "' + self.submit_button.text + '"')
		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load ForgotPasswordForm')

	def read_warning(self):
		text = self.email_warning.text
		if len(text) > 0:
			return self.interpret_warning(text)
		return None

	def interpret_warning(self, warningText):
		warningType = 'undefined'
		if warningText == 'Please enter a valid email address.':
			warningType = 'invalid credentials'

		return {
			'msg': 'forgotPwForm: Submit form warning. ' + warningType,
			'text': warningText,
			'type': warningType,
		}

	def submit_form(self, resetEmail=None, expectedError=None, expectedWarning=None):
		if resetEmail:
			self.email_input.send_keys(resetEmail)
			time.sleep(.4)
			self.submit_button.click()

			return True
		return False


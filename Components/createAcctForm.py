import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class CreateAcctForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_element_by_tag_name('form')
		inputs = self.form.find_elements_by_tag_name('input')
		anchors = self.form.find_elements_by_tag_name('a')
		small = self.form.find_elements_by_tag_name('small')
		# small[2] hidden element

		self.username_input = self.form.find_element_by_id('name')
		self.username_warning = small[0]

		self.email_input = self.form.find_element_by_id('email')
		self.email_warning = small[1]

		self.password_input = self.form.find_element_by_id('password')
		self.password_warning = small[3]

		self.confirm_password_input = self.form.find_element_by_id('confirm_pasword')
		self.confirm_password_warning = small[4]

		self.submit_button = self.form.find_element_by_tag_name('button')

		self.validate()
		return True

	def validate(self):
		failures = []
		if self.submit_button.text != 'Sign Up':
			failures.append('1. Sign Up button. Expecting text "Sign Up", got "' + self.submit_button.text + '"')
		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load CreateAcctForm')

	def read_warning(self):
		inputs = ['username', 'email', 'password', 'confirm password']
		warnings = []
		warning_els = [
			self.username_warning, self.email_warning, self.password_warning, self.confirm_password_warning,
		]
		for i, warning_el in enumerate(warning_els):
			text = warning_el.text
			if len(text) > 0:
				warnings.append({
					'inputName': inputs[i],
					'text': text,
				})
		if len(warnings) > 0:
			return warnings
		return None

	def interpret_warning(self, warningText):
		warningType = 'undefined'
		warningMsg = ''
		if warningText == 'Please enter a valid email address.':
			warningType = 'Invalid credentials'
			warningMsg = 'forgotPwForm: Submit form warning'

		return {
			'msg', warningMsg,
			'text', warningText,
			'type', warningType,
		}


	def enter_credentials(self, credentials):
		if credentials['username'] and credentials['password']:
			self.login_input.send_keys(credentials['username'])
			time.sleep(.4)
			self.password_input.send_keys(credentials['password'])
			time.sleep(.4)
			self.signIn_button.click()
			time.sleep(.4)
			return True
		return False
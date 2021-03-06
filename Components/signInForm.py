import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)


class SignInForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_element_by_tag_name('form')

		# list1 = ["1", 2, 3, 4, 5, 6]

		# dictionary1 = {
		# 	"name": "Elliot",
		# 	"email": "asdf@gmail.com",
		# }

		# email = dictionary1["email"]


		self.username_input = self.form.find_element_by_id('username')

		self.password_input = self.form.find_element_by_id('password')

		self.signIn_button = self.form.find_element_by_tag_name('button')
		self.forgotPassword_link = self.form.find_element_by_tag_name('a')
		# self.validate()
		return True

	def validate(self):
		failures = []
		if self.signIn_button.text != 'Sign In':
			failures.append('1. Sign In button. Expecting text "Sign In", got "' + self.signIn_button.text + '"')
		if self.forgotPassword_link.text != 'Forgot Password':
			failures.append('2. Forgot Password. Expecting text "Forgot Password", got "' + self.forgotPassword_link.text + '"')
		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load SignInForm')

	def read_warning(self):
		inputs = ['Sign In', 'Password']
		warnings = []
		for i, warning_el in enumerate([self.login_warning, self.password_warning]):
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
		if warningText == 'Please enter a valid email address.':
			warningType = 'invalid credentials'
		elif warningText == 'Please enter username.':
			warningType = 'missing username'
		elif warningText == 'Please enter password.':
			warningType = 'missing password'

		return {
			'msg': 'forgotPwForm: Submit form warning. ' + warningMsg,
			'text': warningText,
			'type': warningType,
		}

	def enter_credentials(self, credentials):
		if credentials['username'] and credentials['password']:
			self.username_input.send_keys(credentials['username'])
			time.sleep(.4)
			self.password_input.send_keys(credentials['password'])
			time.sleep(.4)
			# Click doesn't work???
			self.signIn_button.submit()
			time.sleep(.4)
			return True
		return False


import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class CreateAcctForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		anchors = self.form.find_elements_by_tag_name('a')
		small = self.form.find_elements_by_tag_name('small')
		# small[2] hidden element

		self.race_amer_input = inputs[0]
		self.race_asian_input = inputs[1]
		self.race_black_input = inputs[2]
		self.race_native_input = inputs[3]
		self.race_white_input = inputs[4]

		self.ethn_hispanicyes_input = inputs[5]
		self.ethn_hispanicno_input = inputs[6]

		self.race_back_input = inputs[7]

		self.country_input = inputs[8]

		self.city_input = inputs[9]

		self.city_grow_input = inputs[10]

		self.city_adult_input = inputs[11]

		self.religion_input = inputs[12]

		self.marital_input = inputs[13]

		self.education_input = inputs[14]

		self.employment_input = inputs[15]

		self.health_insno_input = inputs[16]
		self.health_insyes_input = inputs[17]

		self.militaryno_input = inputs[18]
		self.militaryyes_input = inputs[19]



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
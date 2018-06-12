import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class FitLvlForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		anchors = self.form.find_elements_by_tag_name('a')
		small = self.form.find_elements_by_tag_name('small')
		# small[2] hidden element

		self.walk_sixhoursyes_radio = inputs[0]
		self.walk_sixhoursno_radio = inputs[1]

		self.walk_fivehoursyes_radio = inputs[2]
		self.walk_fivehoursno_radio = inputs[3]

		self.walk_unassistedyes_radio = inputs[4]
		self.walk_unassistedno_radio = inputs[5]

		self.shopyes_radio = inputs[6]
		self.shopno_radio = inputs[7]

		# self.validate()
		return True

	def validate(self):
		failures = []
		if expectedValues:
			if expectedValues['walk_sixhours'] == 'no' and not self.walk_sixhoursno_radio.get_attribute('checked'):
				failure.append('FitLvlForm: Expecting "no" to walking six or more hours a week')
			elif expectedValues['walk_sixhours'] == 'yes' and not self.walk_sixhoursyes_radio.get_attribute('checked'):
				failure.append('FitLvlForm: Expecting "yes" to walking six or more hours a week')

			if expectedValues['walk_fivehours'] == 'no' and not self.walk_fivehoursno_radio.get_attribute('checked'):
				failure.append('FitLvlForm: Expecting "no" to walking five hours or less a week')
			elif expectedValues['walk_fivehours'] == 'yes' and not self.walk_fivehoursyes_radio.get_attribute('checked'):
				failure.append('FitLvlForm: Expecting "yes" to walking five hours or less a week')

			if expectedValues['walk_unassisted'] == 'no' and not self.walk_unassistedno_radio.get_attribute('checked'):
				failure.append('FitLvlForm: Expecting "no" to walking unassisted')
			elif expectedValues['walk_unassisted'] == 'yes' and not self.walk_unassistedyes_radio.get_attribute('checked'):
				failure.append('FitLvlForm: Expecting "yes" to walking unassisted')

			if expectedValues['shop'] == 'no' and not self.walk_shopno_radio.get_attribute('checked'):
				failure.append('FitLvlForm: Expecting "no" to shoppig unassisted')
			elif expectedValues['shop'] == 'yes' and not self.walk_shopyes_radio.get_attribute('checked'):
				failure.append('FitLvlForm: Expecting "yes" to shopping unassisted')

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
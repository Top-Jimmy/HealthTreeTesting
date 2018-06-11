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
		# small[2] hidden element

		self.status_stable0_input = inputs[0]
		self.status_stable1_input = inputs[1]
		self.status_stable2_input = inputs[2]

		self.status_relapse0_input = inputs[3]
		self.status_relapse1_input = inputs[4]
		self.status_relapse2_input = inputs[5]

		self.status_issues0_input = inputs[6]
		self.status_issues1_input = inputs[7]
		self.status_issues2_input = inputs[8]

		self.condition_heart0_input = inputs[9]
		self.condition_heart1_input = inputs[10]
		self.condition_heart2_input = inputs[11]

		self.condition_lung0_input = inputs[12]
		self.condition_lung1_input = inputs[13]
		self.condition_lung2_input = inputs[14]

		self.condition_kidney0_input = inputs[15]
		self.condition_kidney1_input = inputs[16]
		self.condition_kidney2_input = inputs[17]

		self.condition_diabetes0_input = inputs[18]
		self.condition_diabetes1_input = inputs[19]
		self.condition_diabetes2_input = inputs[20]

		self.condition_blood_pressure0_input = inputs[21]
		self.condition_blood_pressure1_input = inputs[22]
		self.condition_blood_pressure2_input = inputs[23]

		self.condition_blood_clot0_input = inputs[24]
		self.condition_blood_clot1_input = inputs[25]
		self.condition_blood_clot2_input = inputs[26]

		self.condition_neuropathy0_input = inputs[27]
		self.condition_neuropathy1_input = inputs[28]
		self.condition_neuropathy2_input = inputs[29]

		self.condition_other0_input = inputs[30]
		self.condition_other1_input = inputs[31]
		self.condition_other2_input = inputs[32]

		# self.validate()
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
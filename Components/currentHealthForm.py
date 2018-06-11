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

		self.status_stableyes_radio = inputs[0]
		self.status_stableno_radio = inputs[1]
		self.status_stableidk_radio = inputs[2]

		self.status_relapseyes_radio = inputs[3]
		self.status_relapseno_radio = inputs[4]
		self.status_relapseidk_radio = inputs[5]

		self.status_issuesyes_radio = inputs[6]
		self.status_issuesno_radio = inputs[7]
		self.status_issuesidk_radio = inputs[8]

		self.condition_heartyes_radio = inputs[9]
		self.condition_heartno_radio = inputs[10]
		self.condition_heartidk_radio = inputs[11]

		self.condition_lungyes_radio = inputs[12]
		self.condition_lungno_radio = inputs[13]
		self.condition_lungidk_radio = inputs[14]

		self.condition_kidneyyes_radio = inputs[15]
		self.condition_kidneyno_radio = inputs[16]
		self.condition_kidneyidk_radio = inputs[17]

		self.condition_diabetesyes_radio = inputs[18]
		self.condition_diabetesno_radio = inputs[19]
		self.condition_diabetesidk_radio = inputs[20]

		self.condition_blood_pressureyes_radio = inputs[21]
		self.condition_blood_pressureno_radio = inputs[22]
		self.condition_blood_pressureidk_radio = inputs[23]

		self.condition_blood_clotyes_radio = inputs[24]
		self.condition_blood_clotno_radio = inputs[25]
		self.condition_blood_clotidk_radio = inputs[26]

		self.condition_neuropathyyes_radio = inputs[27]
		self.condition_neuropathyno_radio = inputs[28]
		self.condition_neuropathyidk_radio = inputs[29]

		self.condition_otheryes_radio = inputs[30]
		self.condition_otherno_radio = inputs[31]
		self.condition_otheridk_radio = inputs[32]

		# self.validate()
		return True

	def validate(self):
		failures = []
		
		if expectedValues['status_stable'] == 'dont know' and not self.status_stableidk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having a stable condition')
		elif expectedValues['status_stable'] == 'yes' and not self.status_stableyes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having a stable condition')
		elif expectedValues['status_stable'] == 'no' and not self.status_stableno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having a stable condition')

		if expectedValues['status_relapse'] == 'dont know' and not self.status_relapseidk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having a relapse')
		elif expectedValues['status_relapse'] == 'yes' and not self.status_relapseyes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having a relapse')
		elif expectedValues['status_relapse'] == 'no' and not self.status_relapseno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having a relapse')

		if expectedValues['status_issues'] == 'dont know' and not self.status_issuesidk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having health issues')
		elif expectedValues['status_issues'] == 'yes' and not self.status_issuesyes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having health issues')
		elif expectedValues['status_issues'] == 'no' and not self.status_issuesno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having health issues')

		if expectedValues['condition_heart'] == 'dont know' and not self.condition_heartidk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having a stable condition')
		elif expectedValues['condition_heart'] == 'yes' and not self.condition_heartyes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having a stable condition')
		elif expectedValues['condition_heart'] == 'no' and not self.condition_heartno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having a stable condition')

		if expectedValues['condition_lung'] == 'dont know' and not self.condition_lungidk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having a stable condition')
		elif expectedValues['condition_lung'] == 'yes' and not self.condition_lungyes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having a stable condition')
		elif expectedValues['condition_lung'] == 'no' and not self.condition_lungno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having a stable condition')

		if expectedValues['condition_kidney'] == 'dont know' and not self.condition_kidneyidk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having a stable condition')
		elif expectedValues['condition_kidney'] == 'yes' and not self.condition_kidneyyes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having a stable condition')
		elif expectedValues['condition_kidney'] == 'no' and not self.condition_kidneyno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having a stable condition')

		if expectedValues['condition_diabetes'] == 'dont know' and not self.condition_diabetesidk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having a stable condition')
		elif expectedValues['condition_diabetes'] == 'yes' and not self.condition_diabetesyes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having a stable condition')
		elif expectedValues['condition_diabetes'] == 'no' and not self.condition_diabetesno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having a stable condition')

		if expectedValues['condition_blood_pressure'] == 'dont know' and not self.condition_blood_pressureidk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having a stable condition')
		elif expectedValues['condition_blood_pressure'] == 'yes' and not self.condition_blood_pressureyes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having a stable condition')
		elif expectedValues['condition_blood_pressure'] == 'no' and not self.condition_blood_pressureno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having a stable condition')

		if expectedValues['condition_blood_clot'] == 'dont know' and not self.condition_blood_clotidk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having a stable condition')
		elif expectedValues['condition_blood_clot'] == 'yes' and not self.condition_blood_clotyes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having a stable condition')
		elif expectedValues['condition_blood_clot'] == 'no' and not self.condition_blood_clotno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having a stable condition')

		if expectedValues['condition_neuropathy'] == 'dont know' and not self.condition_neuropathyidk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having a stable condition')
		elif expectedValues['condition_neuropathy'] == 'yes' and not self.condition_neuropathyyes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having a stable condition')
		elif expectedValues['condition_neuropathy'] == 'no' and not self.condition_neuropathyno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having a stable condition')

		if expectedValues['condition_other'] == 'dont know' and not self.condition_otheridk_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "dont know" to having a stable condition')
		elif expectedValues['condition_other'] == 'yes' and not self.condition_otheryes_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "yes" to having a stable condition')
		elif expectedValues['condition_other'] == 'no' and not self.condition_otherno_radio.get_attribute('checked'):
			failure.append('CurrentHealthForm: Expecting "no" to having a stable condition')

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
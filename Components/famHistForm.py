import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class FamHistForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		anchors = self.form.find_elements_by_tag_name('a')
		# small[2] hidden element

		self.father_input = inputs[0]

		self.mother_input = inputs[1]

		self.sibling_input = inputs[2]

		self.pat_grandfather_input = inputs[3]

		self.pat_grandmother_input = inputs[4]

		self.mat_grandfather_input = inputs[5]

		self.mat_grandmother_input = inputs[6]

		self.multipleno_input = inputs[7]
		self.multipleyes_input = inputs[8]

		self.smolderno_input = inputs[9]
		self.smolderyes_input = inputs[10]

		self.mgusno_input = inputs[11]
		self.mgusyes_input = inputs[12]

		self.diabetesno_input = inputs[13]
		self.diabetesyes_input = inputs[14]

		self.hyperno_input = inputs[15]
		self.hyperyes_input = inputs[16]

		self.cardiono_input = inputs[17]
		self.cardioyes_input = inputs[18]

		# self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
		if expectedValues:
			if expectedValues['multiple'] == 'no' and not self.multipleno_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "no" to having multiple myeloma')
			elif expectedValues['multiple'] == 'yes' and not self.multipleyes_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "yes" to having multiple myeloma')

			if expectedValues['smoldering'] == 'no' and not self.smolderno_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "no" to having smoldering myeloma')
			elif expectedValues['smoldering'] == 'yes' and not self.smolderyes_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "yes" to having smoldering myeloma')

			if expectedValues['mgus'] == 'no' and not self.mgusno_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "no" to having MGUS')
			elif expectedValues['mgus'] == 'yes' and not self.mgusyes_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "yes" to having MGUS')

			if expectedValues['diabetes'] == 'no' and not self.diabetesno_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "no" to having diabetes')
			elif expectedValues['diabetes'] == 'yes' and not self.diabetesyes_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "yes" to having diabetes')

			if expectedValues['hypertension'] == 'no' and not self.hyperno_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "no" to having hypertension')
			elif expectedValues['hypertension'] == 'yes' and not self.hyperyes_inputj.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "yes" to having hypertension')

			if expectedValues['cardiovascular'] == 'no' and not self.cardiono_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "no" to having cardiovascular disease')
			elif expectedValues['cardiovascular'] == 'yes' and not self.cardioyes_input.get_attribute('checked'):
				failure.append('FamHistForm: Expecting "yes" to having cardiovascular disease')

		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load AboutMeForm')

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


	def enter_info(self, form_info):
		if form_info:
			self.firstname_input.send_keys(form_info['first_name'])
			self.password_input.send_keys(form_info['last_name'])
			if form_info['gender'] == 'male':
				functions.move_to_el(self.male_radio)
			else:
				functions.move_to_el(self.female_radio)
			self.birth_input.send_keys(form_info)['dob']
			self.zipcode_input.send_keys(form_info)['zip_code']
			self.treatment_textarea.send_keys(form_info)['treatment_goals']
			if form_info['assisted'] == True:
				functions.move_to_el(self.cancerCareYes_radio)
			else:
				functions.move_to_el(self.cancerCareNo_radio)

			if form_info['terms'] == True:
				functions.move_to_el(self.termsprivacy_checkbox)

			if form_info['sparkCures'] == True:
				functions.move_to_el(self.SparkCuresterms_checkbox)

			return True
		return False
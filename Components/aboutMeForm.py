import time
import functions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class AboutMeForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		anchors = self.form.find_elements_by_tag_name('a')
		# small[2] hidden element

		self.firstname_input = self.form.find_element_by_id('about_first')
		self.lastname_input = self.form.find_element_by_id('Last')

		self.gender_cont = self.form.find_element_by_id('status')
		self.female_radio = self.gender_cont.find_elements_by_tag_name('input')[0]
		self.male_radio = self.gender_cont.find_elements_by_tag_name('input')[1]


		self.birth_input = inputs[4]

		self.zipcode_input = self.form.find_element_by_id('zip-code')

		self.treatment_textarea = self.form.find_elements_by_tag_name('textarea')

		self.cancerCareYes_radio = inputs[6]
		self.cancerCareNo_radio = inputs[7]

		self.termsprivacy_checkbox = self.form.find_element_by_id('agreed')
		self.SparkCuresterms_checkbox = self.form.find_element_by_id('accepted_understand_clause')

		# self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
		if self.firstname_input.text != 'Sign Up':
			failures.append('1. Sign Up button. Expecting text "Sign Up", got "' + self.firstname_input.text + '"')
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
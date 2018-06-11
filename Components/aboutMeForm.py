import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class AboutMeForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		anchors = self.form.find_elements_by_tag_name('a')
		# small[2] hidden element

		self.firstname_input = self.form.find_element_by_id('about_first')
		self.lastname_input = self.form.find_element_by_id('Last')

		self.gender_cont = self.form.find_element_by_id('status')
		self.female_input = self.gender_cont.find_elements_by_tag_name('input')[0]
		self.male_input = self.gender_cont.find_elements_by_tag_name('input')[1]


		self.birth_input = inputs[4]

		self.zipcode_input = self.form.find_element_by_id('zip-code')

		self.treatment_textarea = self.form.find_elements_by_tag_name('textarea')

		self.cancerCareyes_input = inputs[6]
		self.cancerCareno_input = inputs[7]

		self.termsprivacy_checkbox = self.form.find_element_by_id('agreed')
		self.SparkCuresterms_checkbox = self.form.find_element_by_id('accepted_understand_clause')

		# self.validate()
		return True

	def validate(self):
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
			self.birth_input.send_keys(form_info)['dob']
			self.zipcode_input.send_keys(form_info)['zipcode']
			self.treatment_textarea.send_keys(form_info)['treatment']
			self.cancerCareyes_input.send_keys(form_info)['canceryes']
			self.cancerCareno_input.send_keys(form_info)['canceryno']
			self.termsprivacy_checkbox.send_keys(form_info)['termsprivacy']
			self.SparkCuresterms_checkbox.send_keys(form_info)['terms']



			return True
		return False
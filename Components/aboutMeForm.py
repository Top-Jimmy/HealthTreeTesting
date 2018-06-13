import time
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

		self.firstname_input = self.form.find_element_by_id('about_first')
		self.lastname_input = self.form.find_element_by_id('Last')

		self.gender_cont = self.form.find_element_by_id('status')
		self.female_radio = self.gender_cont.find_elements_by_tag_name('input')[0]
		self.male_radio = self.gender_cont.find_elements_by_tag_name('input')[1]

		self.birth_input = inputs[4]

		self.zipcode_input = self.form.find_element_by_id('zip-code')

		self.treatment_textarea = self.form.find_elements_by_tag_name('textarea')

		self.load_cancer_care()

		self.termsprivacy_checkbox = self.form.find_element_by_id('agreed')
		self.SparkCuresterms_checkbox = self.form.find_element_by_id('accepted_understand_clause')

		# self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
		if expectedValues:
			if self.firstname_input.get_attribute('value') != expectedValues['first_name']:
				failures.append('AboutMeForm: Expecting first name "' + expectedValues['first_name'] + '", got "' + self.firstname_input.get_attribute('value') + '"')
			if self.lastname_input.get_attribute('value') != expectedValues['last_name']:
				failures.append('AboutMeForm: Expecting last name "' + expectedValues['last_name'] + '", got "' + self.lastname_input.get_attribute('value') + '"')
			if self.birth_input.get_attribute('value') != expectedValues['dob']:
				failures.append('AboutMeForm: Expecting date of birth "' + expectedValues['dob'] + '", got "' + self.birth_input.get_attribute('value') + '"')
			if self.zipcode_input.get_attribute('value') != expectedValues['zip_code']:
				failures.append('AboutMeForm: Expecting zip code "' + expectedValues['zip_code'] + '", got"' + self.zipcode_input.get_attribute('value') + '"')

			if expectedValues['gender'] == 'male' and not self.male_radio.get_attribute('checked'):
				failure.append('AboutMeForm: Expecting gender "male"')
			elif expectedValues['gender'] == 'female' and not self.female_radio.get_attribute('checked'):
				failure.append('AboutMeForm: Expecting gender "female"')

			if expectedValues['assisted'] == 'no' and not self.cancerCareNo_radio('checked'):
				failure.append('AboutMeForm: Expecting "no" to family assistance')
			elif expectedValues['assisted'] == 'yes' and not self.cancerCareYes_radio.get_attribute('checked'):
				failure.append('AboutMeForm: Expecting "yes" to family assistance')

			if expectedValues['terms'] != self.termsprivacy_checkbox.get_attribute('checked'):
				failure.append('AboutMeForm: Expecting "' + str(expectedValues['terms']) + '" Terms and Conditions')

			if expectedValues['sparkCures'] != self.SparkCuresterms_checkbox.get_attribute('checked'):
				failure.append('AboutMeForm: Expecting "' + str(expectedVaues['sparkCures']) + '" Terms and Conditions')

		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load AboutMeForm')

	def read_warnings(self):
		warnings = []
		# Look for elements w/ class text-error

		# For each element, check if it has text.

		# If it has text, add it to warnings
			# warnings.append(text)
		# pass warnings into interpret_warning() and return the response

	def interpret_warning(self, warnings):
		warningObjects = []
		# Loop through each warning in warnings

		# If warning matches error for
			# 1. missing terms
			# 2. missing sparkCures
			# 3. first name
			# 4. last name
			# etc...

		# create warning object

		# return all warning objects

		warningType = 'undefined'
		warningMsg = ''
		if warningText == 'Please enter a valid email address.':
			warningType = 'Invalid credentials'
			warningMsg = 'forgotPwForm: Submit form warning'

		warningObjects.append({
			'msg', warningMsg,
			'text', warningText,
			'type', warningType,
		});
		return warningObjects

	def load_cancer_care(self):
		inputs = self.form.find_elements_by_tag_name('input')

		try:
			self.caregiver_name_input = self.form.find_element_by_id('c_name')
			self.caregiver_phone_input = self.form.find_element_by_id('c_phone')
			self.caregiver_email_input = self.form.find_element_by_id('c_email')
		except NoSuchElementException:
			self.caregiver_name_input = None
			self.caregiver_phone_input = None
			self.caregiver_email_input = None

		self.cancerCareYes_radio = inputs[6]
		self.cancerCareNo_radio = inputs[7]

	def enter_info(self, form_info):
		if form_info:
			self.firstname_input.send_keys(form_info['first_name'])
			self.password_input.send_keys(form_info['last_name'])
			if form_info['gender'] == 'male':
				self.male_radio.click()
			else:
				self.female_radio.click()
			self.birth_input.send_keys(form_info)['dob']
			self.zipcode_input.send_keys(form_info)['zip_code']
			self.treatment_textarea.send_keys(form_info)['treatment_goals']

			if form_info['assisted']['value'] == True:
				self.cancerCareYes_radio.click()
				self.load_cancer_care()
				# Does credentials have caregiver info?
				if form_info['assisted']['name']:
					self.caregiver_name_input.send_keys(form_info['assisted']['name'])
				if form_info['assitsted']['phone']:
					self.caregiver_phone_input.send_keys(form_info['assisted']['phone'])
				if form_info['assisted']['email']:
					self.caregiver_email_input.send_keys(form_info['assisted']['email'])

				# if yes, enter it into inputs loaded in load_cancer_care()

			else:
				self.cancerCareNo_radio.click()

			if form_info['terms'] == True:
				self.termsprivacy_checkbox.click()

			if form_info['sparkCures'] == True:
				self.SparkCuresterms_checkbox.click()

			return True
		return False
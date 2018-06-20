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
		rows = self.form.find_elements_by_class_name('form-group')

		self.firstname_input = self.form.find_element_by_id('about_first')
		self.lastname_input = self.form.find_element_by_id('Last')

		container = self.driver.find_element_by_id('gender_radio_group')
		labels = container.find_elements_by_tag_name('label')
		self.female_radio = labels[0]
		self.male_radio = labels[1]

		dob_cont = self.driver.find_element_by_class_name('mui-select')
		self.dob_input = dob_cont.find_element_by_tag_name('input')

		self.zipcode_input = self.form.find_element_by_id('zip-code')

		self.treatment_textarea = self.form.find_element_by_tag_name('textarea')

		self.load_cancer_care()

		# Terms of Use and Privacy Policy checkboxes and links
		label_conts = self.form.find_elements_by_class_name('checkbox-custom-label')
		self.termsprivacy_checkbox = self.form.find_element_by_id('agreed')
		terms_links = label_conts[0].find_elements_by_tag_name('a')
		self.ht_terms_link = terms_links[0]
		self.ht_privacy_link = terms_links[1]

		self.SparkCuresterms_checkbox = self.form.find_element_by_id('accepted_understand_clause')
		spark_links = label_conts[1].find_elements_by_tag_name('a')
		self.spark_terms_link = spark_links[0]
		self.spark_privacy_link = spark_links[1]

		self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
		if expectedValues:
			if self.firstname_input.get_attribute('value') != expectedValues['first_name']:
				failures.append('AboutMeForm: Expecting first name "' + expectedValues['first_name'] + '", got "' + self.firstname_input.get_attribute('value') + '"')
			if self.lastname_input.get_attribute('value') != expectedValues['last_name']:
				failures.append('AboutMeForm: Expecting last name "' + expectedValues['last_name'] + '", got "' + self.lastname_input.get_attribute('value') + '"')
			if self.dob_input.get_attribute('value') != expectedValues['dob']:
				failures.append('AboutMeForm: Expecting date of birth "' + expectedValues['dob'] + '", got "' + self.dob_input.get_attribute('value') + '"')
			if self.zipcode_input.get_attribute('value') != expectedValues['zip_code']:
				failures.append('AboutMeForm: Expecting zip code "' + expectedValues['zip_code'] + '", got"' + self.zipcode_input.get_attribute('value') + '"')

			if expectedValues['gender'] == 'male' and not self.male_radio.get_attribute('checked'):
				failure.append('AboutMeForm: Expecting gender "male"')
			elif expectedValues['gender'] == 'female' and not self.female_radio.get_attribute('checked'):
				failure.append('AboutMeForm: Expecting gender "female"')

			if expectedValues['assisted'] == 'no' and not self.cancerCareNo_radio.get_attribute('checked'):
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
		warningElements = self.form.find_elements_by_class_name('text-error')

		# For each element, check if it has text.
		for element in warningElements:
			if element.text != '':
				warnings.append(element.text)

		# pass warnings into interpret_warning()
		#  return the response
		return self.interpret_warning(warnings)

	def interpret_warning(self, warnings):
		warningObjects = []
		# Loop through each warning in warnings
		for warningText in warnings:
			warningType = 'undefined'
			if warningText == 'Please enter first name.':
				warningType = 'Missing first name'
			elif warningText == 'Please enter last name.':
				warningType = 'Missing last name'
			elif warningText == 'Please enter valid date format (MM/DD/YYYY).':
				warningType = 'Missing date'
			elif warningText == 'Please enter zip code.':
				warningType = 'Missing zip code'
			elif warningText == 'Please share your treatment goals.':
				warningType = 'Missing treatment goals'
			elif warningText == 'Please enter name.':
				warningType = 'Missing caregiver name'
			elif warningText == 'Please enter phone number.':
				warningType = 'Missing caregiver number'
			elif warningText == 'Please enter email.':
				warningType = 'Missing caregiver email'
			elif warningText == 'Please check privacy policy.':
				warningType = 'Missing privacy agreement'
			elif warningText == 'Please check license agreement.':
				warningType = 'Missing license agreement'

			# create warning object
			warningObjects.append({
				'msg': 'aboutMeForm: Submit form warning',
				'text': warningText,
				'type': warningType,
			});
		# return all warning objects
		return warningObjects

	def load_cancer_care(self):
		cont = self.form.find_element_by_id('cancerCare_radio_group')
		inputs = cont.find_elements_by_tag_name('input')
		self.cancerCareYes_radio = inputs[0]
		self.cancerCareNo_radio = inputs[1]

		# caregiver inputs only there if radio group is set to 'Yes'
		try:
			self.caregiver_name_input = self.form.find_element_by_id('c_name')
			self.caregiver_phone_input = self.form.find_element_by_id('c_phone')
			self.caregiver_email_input = self.form.find_element_by_id('c_email')
		except NoSuchElementException:
			self.caregiver_name_input = None
			self.caregiver_phone_input = None
			self.caregiver_email_input = None

	def enter_info(self, form_info):
		if form_info:
			self.firstname_input.clear()
			self.firstname_input.send_keys(form_info['first_name'])
			self.lastname_input.clear()
			self.lastname_input.send_keys(form_info['last_name'])
			if form_info['gender'] == 'male':
				self.male_radio.click()
			else:
				self.female_radio.click()
			self.dob_input.clear()
			self.dob_input.send_keys(form_info['dob'])
			self.zipcode_input.clear()
			self.zipcode_input.send_keys(form_info['zip_code'])
			self.treatment_textarea.clear()
			self.treatment_textarea.send_keys(form_info['treatment_goals'])

			# if form_info['assisted']['value'] == True:
			# 	self.cancerCareYes_radio.click()
			# 	self.load_cancer_care()
			# 	# Does credentials have caregiver info?
			# 	if form_info['assisted']['name']:
			# 		self.caregiver_name_input.clear()
			# 		self.caregiver_name_input.send_keys(form_info['assisted']['name'])
			# 	if form_info['assitsted']['phone']:
			# 		self.caregiver_phone_input.clear()
			# 		self.caregiver_phone_input.send_keys(form_info['assisted']['phone'])
			# 	if form_info['assisted']['email']:
			# 		self.caregiver_email_input.clear()
			# 		self.caregiver_email_input.send_keys(form_info['assisted']['email'])

				# if yes, enter it into inputs loaded in load_cancer_care()

			# else:
			# 	self.cancerCareNo_radio.click()
			if form_info['terms'] != self.termsprivacy_checkbox.is_selected():
				self.termsprivacy_checkbox.click()

			if form_info['sparkCures'] != self.SparkCuresterms_checkbox.is_selected():
				self.SparkCuresterms_checkbox.click()

			return True
		return False
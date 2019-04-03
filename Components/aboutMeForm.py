import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class AboutMeForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues):
		self.form = self.driver.find_element_by_id('page-content-wrapper')
		# inputs = self.form.find_elements_by_tag_name('input')
		# anchors = self.form.find_elements_by_tag_name('a')

		self.personalinfo_table = self.form.find_element_by_class_name('profile_1')
		self.edit_personal_button = self.personalinfo_table.find_element_by_tag_name('button')

		self.load_personal_info()

		treatment_goals = self.personalinfo_table.find_element_by_id('right_div')
		self.treatment_goals_input = treatment_goals.find_element_by_tag_name('span')

		self.myeloma_centers_table = self.form.find_element_by_class_name('profile_2')
		self.view_myeloma_button = self.myeloma_centers_table.find_element_by_tag_name('button')

		self.family_table = self.form.find_element_by_class_name('profile_3')
		self.edit_family_button = self.family_table.find_element_by_tag_name('button')

		self.load_family_info()

		self.terms_conditions_header = self.form.find_element_by_class_name('profile_4')
		self.edit_terms_button = self.terms_conditions_header.find_element_by_tag_name('button')

		# self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
		if expectedValues:
			if self.firstname_input.get_attribute('value') != expectedValues['first_name']:
				failures.append('AboutMeForm: Expecting first name "' + expectedValues['first_name'] + '", got "' + self.firstname_input.get_attribute('value') + '"')
			if self.middlename_input.get_attribute('value') != expectedValues['middle_name']:
				failures.append('AboutMeForm: Expecting last name "' + expectedValues['middle_name'] + '", got "' + self.middlename_input.get_attribute('value') + '"')
			if self.lastname_input.get_attribute('value') != expectedValues['last_name']:
				failures.append('AboutMeForm: Expecting last name "' + expectedValues['last_name'] + '", got "' + self.lastname_input.get_attribute('value') + '"')
			if self.dob_input.get_attribute('value') != expectedValues['dob']:
				failures.append('AboutMeForm: Expecting date of birth "' + expectedValues['dob'] + '", got "' + self.dob_input.get_attribute('value') + '"')
			if self.zipcode_input.get_attribute('value') != expectedValues['zip_code']:
				failures.append('AboutMeForm: Expecting zip code "' + expectedValues['zip_code'] + '", got"' + self.zipcode_input.get_attribute('value') + '"')

			if expectedValues['gender'] != self.gender_values[0]:
				failures.append('AboutMeForm: Expecting gender "' + str(expectedValues['gender']) + '". Radio loaded: ' + str(self.gender_values[0]))

			if expectedValues['assisted'] == 'no' and not self.cancerCareNo_radio.get_attribute('checked'):
				failures.append('AboutMeForm: Expecting "no" to family assistance')
			elif expectedValues['assisted'] == 'yes' and not self.cancerCareYes_radio.get_attribute('checked'):
				failures.append('AboutMeForm: Expecting "yes" to family assistance')

			if expectedValues['terms'] != self.termsprivacy_checkbox.get_attribute('checked'):
				failures.append('AboutMeForm: Expecting "' + str(expectedValues['terms']) + '" Terms and Conditions. Loaded ' + str(self.termsprivacy_checkbox.get_attribute('checked')))

			if expectedValues['sparkCures'] != self.SparkCuresterms_checkbox.get_attribute('checked'):
				failures.append('AboutMeForm: Expecting "' + str(expectedValues['sparkCures']) + '" SparkCures. Loaded ' + str(self.SparkCuresterms_checkbox.get_attribute('checked')))

		if len(failures) > 0:
			for failure in failures:
				print(failure)
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

	def tooltip(self):
		self.academic_tooltip.click()
		p = self.academic_tooltip.find_element_by_tag_name('p')
		if p.text != 'See the closest Cancer Treatment Centers or Specialist to your zip code.':
			print('tooltip not clicked correctly:' + str(p.text))
			return False
		return True


	def enter_info(self, form_info):
		if form_info:
			self.firstname_input.clear()
			self.firstname_input.send_keys(form_info['first_name'])
			self.middlename_input.clear()
			self.middlename_input.send_keys(form_info['middle_name'])
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

			if form_info['assisted']['value'] == True:
				self.cancerCareYes_radio.click()
				self.load_cancer_care()
				# Does credentials have caregiver info?
				if form_info['assisted']['name']:
					self.caregiver_name_input.clear()
					self.caregiver_name_input.send_keys(form_info['assisted']['name'])
				if form_info['assitsted']['phone']:
					self.caregiver_phone_input.clear()
					self.caregiver_phone_input.send_keys(form_info['assisted']['phone'])
				if form_info['assisted']['email']:
					self.caregiver_email_input.clear()
					self.caregiver_email_input.send_keys(form_info['assisted']['email'])

				# if yes, enter it into inputs loaded in load_cancer_care()

			else:
				self.cancerCareNo_radio.click()
			if form_info['terms'] != self.termsprivacy_checkbox.is_selected():
				self.termsprivacy_checkbox.click()

			if form_info['sparkCures'] != self.SparkCuresterms_checkbox.is_selected():
				self.SparkCuresterms_checkbox.click()

			return True
		return False

	def load_personal_info(self):
		self.personal_info = []
		table = self.personalinfo_table.find_element_by_class_name('researcher_1')
		rows = table.find_elements_by_class_name('row')
		for row in rows:
			personal_information = row.find_elements_by_tag_name('div')[1]
			self.personal_info.append(personal_information.text.lower()) 
		return self.personal_info
			
	def load_family_info(self):
		self.family_info = []
		tables = self.family_table.find_elements_by_class_name('researcher_1')
		for table in tables:
			rows = table.find_elements_by_class_name('row')
			for row in rows:
				family_information = row.find_elements_by_tag_name('div')[1]
				self.family_info.append(family_information.text.lower()) 
		return self.family_info

		



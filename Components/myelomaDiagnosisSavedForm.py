import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
import datePicker

# Form on 'Myeloma Diagnosis' displaying user's saved diagnosis info

class MyelomaDiagnosisSavedForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues):
		self.form = self.driver.find_element_by_id('diagnosis_form')
		add_buttons = self.form.find_elements_by_class_name('custom_addDiagnoisisButton')

		self.diagnosis_table = self.form.find_element_by_class_name('diagnosis-frst-table')
		self.diagnoses = self.load_diagnoses()
		self.add_diagnosis_button = add_buttons[0]

		self.physician_table = self.form.find_element_by_class_name('diagnosis-scnd-table')
		self.physicians = self.load_physicians()
		self.add_physician_button = add_buttons[1]

		# self.validate(expectedValues)
		return True

	# def validate(self, expectedValues):
	# 	if expectedValues:
	# 		failures = []
	# 		if expectedValues['newly_diagnosed'] == 'no' and not self.newly_diagnosedNo.get_attribute('checked')
	# 			failure.append('MyelDiagForm: Expecting "no" to being newly diagnosed')

	# 		if len(failures) > 0:
	# 			print(failures)
	# 			raise NoSuchElementException('Failed to load CreateAcctForm')

	def load_diagnoses(self):
		diagnoses = []
		if self.diagnosis_table:
			rows = self.diagnosis_table.find_elements_by_class_name('borderTableRow')
			for i, row in enumerate(rows):
				diagnosis = {}
				# Data
				diagnosis['date'] = rows[i].find_element_by_class_name('diagnosis-date-sec').text
				diagnosis['type'] = rows[i].find_element_by_class_name('diagnosis-type-sec').text
				diagnosis['bone lesions'] = rows[i].find_element_by_class_name('diagnosis-bone-sec')
				diagnosis['facility'] = rows[i].find_element_by_class_name('diagnosis-facility-sec')
				diagnosis['city'] = rows[i].find_element_by_class_name('diagnosis-city-sec')
				diagnosis['state'] = rows[i].find_element_by_class_name('diagnosis-state-sec')

				# Actions
				buttons = rows[i].find_elements_by_tag_name('button')
				diagnosis['edit'] = buttons[0]
				diagnosis['delete'] = buttons[1]

		return diagnoses

	def load_physicians(self):
		physicians = []
		if self.physician_table:
			rows = self.physician_table.find_elements_by_class_name('borderTableRow')
			for i, row in enumerate(rows):
				physician = {}
				# Data
				physician['name'] = rows[i].find_element_by_class_name('phy_name').text
				physician['facility'] = rows[i].find_element_by_class_name('phy_fac_name').text
				physician['city'] = rows[i].find_element_by_class_name('phy_city')
				physician['state'] = rows[i].find_element_by_class_name('phy_state')

				# actions
				physician['delete'] = rows[i].find_element_by_tag_name('button')
		return physicians

	# def read_warning(self):
	# 	inputs = ['username', 'email', 'password', 'confirm password']
	# 	warnings = []
	# 	warning_els = [
	# 		self.username_warning, self.email_warning, self.password_warning, self.confirm_password_warning,
	# 	]
	# 	for i, warning_el in enumerate(warning_els):
	# 		text = warning_el.text
	# 		if len(text) > 0:
	# 			warnings.append({
	# 				'inputName': inputs[i],
	# 				'text': text,
	# 			})
	# 	if len(warnings) > 0:
	# 		return warnings
	# 	return None

	# def interpret_warning(self, warningText):
	# 	warningType = 'undefined'
	# 	warningMsg = ''
	# 	if warningText == 'Please enter a valid email address.':
	# 		warningType = 'Invalid credentials'
	# 		warningMsg = 'forgotPwForm: Submit form warning'

	# 	return {
	# 		'msg', warningMsg,
	# 		'text', warningText,
	# 		'type', warningType,
	# 	}

	def submit(self, formInfo):
		if formInfo:
			if formInfo['newly_diagnosed'] is not None:
				if formInfo['newly_diagnosed']:
					self.newlyDiagnosedYes_radio.click()
				else:
					self.newlyDiagnosedNo_radio.click()

			if formInfo['diagnosis_date'] is not None:
				self.dateDiagnosis_input.click()
				datePicker = datePicker.DatePicker(self.driver)
				datePicker.setDate(formInfo['diagnosis_date'])

			if formInfo['first_diagnosis'] is not None:
				self.firstDiagnosis_input.click()
				# todo: dropdown component

			if formInfo['high_risk'] is not None:
				high_risk = formInfo['high_risk']
				if high_risk == 'no':
					highRisk1_radio.click()
				elif high_risk == 'yes':
					highRisk2_radio.click()
				else:
					highRisk3_radio.click()

			if formInfo['transplant_eligible'] is not None:
				eligible = formInfo['transplant_eligible']
				if eligible == 'no':
					stemCell1_radio.click()
				elif eligible == 'yes':
					stemCell2_radio.click()
				else:
					stemCell3_radio.click()

			if formInfo['bone_lesions'] is not None:
				bone_lesions = formInfo['bone_lesions']
				if bone_lesions == 'no lesions':
					self.boneLesion0_radio.click()
				elif bone_lesions == '5 or less':
					self.boneLesion1_radio.click()
				elif bone_lesions == '6 or more':
					self.boneLesion2_radio.click()
				else:
					self.boneLesion3_radio.click()

			if formInfo['diagnosis_location']: # Empty dict should evaluate to False
				location = formInfo['diagnosis_location']
				if location['facility']:
					self.facility_input.clear()
					self.facility_input.send_keys(location['facility'])
				if location['city']:
					self.facility_city_input.clear()
					self.facility_city_input.send_keys(location['city'])
				if location['state']:
					# todo: state dropdown
					pass

			if formInfo['additional_diagnosis'] is not None:
				add_diag = formInfo['additional_diagnosis']
				if not add_diag:
					add_diagNo_radio.click()
				else:
					add_diagYes_radio.click()
					if formInfo['additional_diagnoses']:
						pass
						# todo: recursive function: check for errors, load new inputs, check for additional_diagnoses, enter data

			if formInfo['physicians']:
				# todo: handle multiple physician inputs. load into list
				# todo: handle adding multiple physicians
				for i, physician in enumerate(formInfo['physicians']):
					if physician['name']:
						self.phys_name_input.clear()
						self.phys_name_input.send_keys(physician['name'])
					if physician['facility']:
						self.phys_facility_input.clear()
						self.phys_facility_input.send_keys(physician['facility'])
					if physician['city']:
						self.phys_city_input.clear()
						self.phys_city_input.send_keys(physician['city'])
					if physician['state']:
						self.phys_state_input.clear()
						self.phys_state_input.send_keys(physician['state'])

					self.continue_button.click()
			return True
		return False

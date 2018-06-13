import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver import ActionChains as AC
import datePicker

# Form on 'Myeloma Diagnosis' when user has not saved diagnosis info.

class MyelomaDiagnosisFreshForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues=None):
		self.form = self.driver.find_element_by_id('diagnosis_form')
		inputs = self.form.find_elements_by_tag_name('input')
		dropdowns = self.form.find_elements_by_class_name('Select-placeholder')

		self.newlyDiagnosedNo_radio = self.form.find_element_by_id('newly_diagnosedNo')
		self.newlyDiagnosedYes_radio = self.form.find_element_by_id('newly_diagnosedYes')

		self.dateDiagnosis_cont = self.form.find_element_by_class_name('mnth-datepicker')
		self.dateDiagnosis_input = self.dateDiagnosis_cont.find_element_by_tag_name('input')

		self.firstDiagnosis_input = inputs[3]
		self.firstDiagnosis_clicker = dropdowns[0]

		self.highRisk1_radio = self.form.find_element_by_id('highRisk1')
		self.highRisk2_radio = self.form.find_element_by_id('highRisk2')
		self.highRisk3_radio = self.form.find_element_by_id('highRisk3')

		self.stemCell1_radio = self.form.find_element_by_id('stemCell1')
		self.stemCell2_radio = self.form.find_element_by_id('stemCell2')
		self.stemCell3_radio = self.form.find_element_by_id('stemCell3')

		self.boneLesion0_radio = self.form.find_element_by_id('0')
		self.boneLesion1_radio = self.form.find_element_by_id('1')
		self.boneLesion2_radio = self.form.find_element_by_id('2')
		self.boneLesion3_radio = self.form.find_element_by_id('3')

		self.facility_input = self.form.find_element_by_id('facility_name')
		self.facility_city_input = self.form.find_element_by_id('Last')
		self.facility_state_input = inputs[15]
		self.facility_state_clicker = dropdowns[1]

		self.add_diagNo_radio = self.form.find_element_by_id('yesno0')
		self.add_diagYes_radio = self.form.find_element_by_id('yesno1')

		# todo handle loading multiple diagnosis inputs, delete diagnosis button, add diagnosis action

		# Physician Name
		self.phys_name_cont = self.form.find_element_by_class_name('rbt-input-hint-container')
		phys_inputs = self.phys_name_cont.find_elements_by_tag_name('input')
		# self.phys_name_input = self.form.find_element_by_id('physician_name_0')
		# self.phys_name_hiddenInput = self.form.find_element_by_class_name('rbt-input-hint')
		self.phys_name_input = self.form.find_element_by_id('physician_name_0')
		self.phys_name_hiddenInput = phys_inputs[1]

		# Physician Facility
		cont = self.form.find_element_by_id('facility_name_0')
		self.phys_facility_input = cont.find_element_by_tag_name('input')

		# Physician City
		cont = self.form.find_element_by_id('city0')
		self.phys_city_input = cont.find_element_by_tag_name('input')

		# Physician State
		cont = self.form.find_element_by_id('state0')
		self.phys_state_input = cont.find_element_by_tag_name('input')
		self.phys_state_clicker = dropdowns[2]
		# todo: load additional physician button

		button_cont = self.form.find_element_by_class_name('submit_button')
		self.continue_button = button_cont.find_element_by_tag_name('button')

		# self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
		if expectedValues:
			if expectedValues['newly_diagnosed'] == 'no' and not self.newly_diagnosedNo_radio.get_attribute('checked')
				failure.append('MyelDiagForm: Expecting "no" to being newly diagnosed')
			elif expectedValues['newly_diagnosed'] == 'yes' and not self.newly_diagnosedYes_radio.get_attribute('checked')
				failure.append('MyelDiagForm: Expecting "yes" to being newly diagnosed')

			if self.dateDiagnosis_form-control.get_attribute('value') != expectedValues['date']:
				failures.append('MyelDiagForm: Expecting date of diagnosis "' + expectedValues['date'] + '", got "' + self.dateDiagnosis_form-control.get_attribute('value') + '"')

			if expectedValues['high_risk'] == 'no' and not self.highRisk1_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "no" to being high risk')
			elif expectedValues['high_risk'] == 'yes' and not self.highRisk2_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "yes" to being high risk')
			elif expectedValues['high_risk'] == 'I dont know' and not self.highRisk3_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "I dont know to being high risk')

			if expectedValues['stem_cell'] == 'no' and not self.stemCell1_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "no" to being eligible for stem cell')
			elif expectedValues['stem_cell'] == 'yes' and not self.stemCell2_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "yes" to being eligible for stem cell')
			elif expectedValues['stem_cell'] == 'I dont know' and not self.stemCell3_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "I dont know" to being eligible for stem cell')

			if expectedValues['lesions'] == 'no lesions' and not self.boneLesion0_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "no lesions" to # of bone lesions')
			elif expectedValues['lesions'] == '5 or less' and not self.boneLesion1_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "5 or less" to # of bone lesions')
			elif expectedValues['lesions'] == '6 or more' and not self.boneLesion2_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "6 or more" to # of bone lesions')
			elif expectedValues['lesions'] == 'I dont know' and not self.boneLesion3_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "I dont know" to # of bone lesions')

			if self.facility_input.get_attribute('value') != expectedValues['facility']:
				failure.append('MyelDiagForm: Expecting facility "' + expectedValues['facility'] + '", got "' + self.facility_input.get_attribute('value') + '"')
			if self.city_input.get_attribute('value') != expectedValues['city']:
				failure.append('MyelDiagForm: Expecting city "' + expectedValues['city'] + '", got "' + self.city_input.get_attribute('value') + '"')
			if self.state_input.get_attribute('value') != expectedValues['state']:
				failure.append('MyelDiagForm: Expecfting state "' + expectedValues['state'] + '", got "' + self.state_input.get_attribute('value') + '"')

			if expectedValues['additional'] == 'no' and not self.add_diagno_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "no" to an additional diagnosis')
			elif expectedValues['additional'] == 'yes' and not self.add_diagyes_radio.get_attribute('checked')
				failure.append('MyelDiagForm: Expecting "yes" to an additional diagnosis')

			if self.phys_name_input.get_attribute('value') != expectedValues['phys_name']:
				failure.append('MyelDiagForm: Expecting physician name "' + expectedValues['phys_name'] + '", got "' + self.phys_name_input.get_attribute('value') + '"')
			if self.phys_facility_input.get_attribute('value') != expectedValues['phys_facility']:
				failure.append('MyelDiagForm: Expecting physician facility "' + expectedValues['phys_facility'] + '", got "' + self.phys_facility_input.get_attribute('value') + '"')
			if self.phys_city_input.get_attribute('value') != expectedValues['phys_city']:
				failure.append('MyelDiagForm: Expecting physician city "' + expectedValues['phys_city'] + '", got "' self.phys_city_input.get_attribute('value') + '"')
			if self.phys_state_input.get_attribute('value') != expectedValues['phys_state']:
				failure.append('MyelDiagForm: Expecting physician state "' + expectedValues['phys_state'] + '", got "' self.phys_state_input.get_attribute('value') + '"')

		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load CreateAcctForm')


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
				# raw_input('clicking date input')
				self.dateDiagnosis_input.click()
				# raw_input('clicked date input. loading date picker')
				picker = datePicker.DatePicker(self.driver)
				# raw_input('loaded date picker. setting date')
				picker.set_date(formInfo['diagnosis_date'])

			if formInfo['first_diagnosis'] is not None:
				self.firstDiagnosis_clicker.click()
				# todo: dropdown component

			if formInfo['high_risk'] is not None:
				high_risk = formInfo['high_risk']
				if high_risk == 'no':
					self.highRisk1_radio.click()
				elif high_risk == 'yes':
					self.highRisk2_radio.click()
				else:
					self.highRisk3_radio.click()

			if formInfo['transplant_eligible'] is not None:
				eligible = formInfo['transplant_eligible']
				if eligible == 'no':
					self.stemCell1_radio.click()
				elif eligible == 'yes':
					self.stemCell2_radio.click()
				else:
					self.stemCell3_radio.click()

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
					self.add_diagNo_radio.click()
				else:
					self.add_diagYes_radio.click()
					if formInfo['additional_diagnoses']:
						pass
						# todo: recursive function: check for errors, load new inputs, check for additional_diagnoses, enter data

			if formInfo['physicians']:
				# todo: handle multiple physician inputs. load into list
				# todo: handle adding multiple physicians
				for i, physician in enumerate(formInfo['physicians']):
					if physician['name']:
						self.phys_name_input.click()
						AC(self.driver).send_keys(physician['name']).perform()

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

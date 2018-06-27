import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datePicker


# Form on 'Myeloma Diagnosis' when user has not saved diagnosis info.

class MyelomaDiagnosisFreshForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues=None):
		self.form = self.driver.find_element_by_id('diagnosis_form')
		self.load_state()

		self.dateDiagnosis_cont = self.form.find_element_by_class_name('mnth-datepicker')
		self.dateDiagnosis_input = self.dateDiagnosis_cont.find_element_by_tag_name('input')
		self.load_first_diagnosis_dropdown()

		if self.state == 'new_diagnosis':
			self.stable_no_input = self.form.find_element_by_id('stablehighRisk1')
			self.stable_yes_input = self.form.find_element_by_id('stablehighRisk2')
			self.stable_idk_input = self.form.find_element_by_id('stablehighRisk3')

			self.mprotein_no_input = self.form.find_element_by_id('relapsing_highRisk1')
			self.mprotein_yes_input = self.form.find_element_by_id('relapsing_highRisk2')
			self.mprotein_idk_input = self.form.find_element_by_id('relapsing_highRisk3')

			self.recent_pain_no_input = self.form.find_element_by_id('relapsing_issue_highRisk1')
			self.recent_pain_yes_input = self.form.find_element_by_id('relapsing_issue_highRisk2')
			self.recent_pain_idk_input = self.form.find_element_by_id('relapsing_issue_highRisk3')

		self.boneLesion0_radio = self.form.find_element_by_id('0')
		self.boneLesion1_radio = self.form.find_element_by_id('1')
		self.boneLesion2_radio = self.form.find_element_by_id('2')
		self.boneLesion3_radio = self.form.find_element_by_id('3')

		self.highRisk1_radio = self.form.find_element_by_id('highRisk1')
		self.highRisk2_radio = self.form.find_element_by_id('highRisk2')
		self.highRisk3_radio = self.form.find_element_by_id('highRisk3')

		self.stemCell1_radio = self.form.find_element_by_id('stemCell1')
		self.stemCell2_radio = self.form.find_element_by_id('stemCell2')
		self.stemCell3_radio = self.form.find_element_by_id('stemCell3')

		self.facility_input = self.form.find_element_by_id('facility_name')
		self.facility_city_input = self.form.find_element_by_id('Last')
		self.load_facility_state()

		self.add_diagNo_radio = self.form.find_element_by_id('yesno0')
		self.add_diagYes_radio = self.form.find_element_by_id('yesno1')

		return self.validate(expectedValues)

	def validate(self, expectedValues):
		failures = []
		if expectedValues:
			# Right # of diagnoses and physicians?
			#
			# if len(expectedDiagnoses) != len(self.diagnoses):
			# 	failures.append('MyelDiagSavedForm: Expected ' + str(len(expectedDiagnoses)) + ' diagnoses. Form has ' + str(len(self.diagnoses)))
			if len(expectedValues['physicians']) != len(self.physicians):
				failures.append('MyelDiagForm: Expected ' + str(len(expectedPhysicians)) + ' physicians. Form has ' + str(len(self.physicians)))


			# if expectedValues['newly_diagnosed'] == 'no' and not self.newly_diagnosedNo_radio.get_attribute('checked'):
			# 	failure.append('MyelDiagForm: Expecting "no" to being newly diagnosed')
			# elif expectedValues['newly_diagnosed'] == 'yes' and not self.newly_diagnosedYes_radio.get_attribute('checked'):
			# 	failure.append('MyelDiagForm: Expecting "yes" to being newly diagnosed')

			if self.dateDiagnosis_form-control.get_attribute('value') != expectedValues['date']:
				failures.append('MyelDiagForm: Expecting date of diagnosis "' + expectedValues['date'] + '", got "' + self.dateDiagnosis_form-control.get_attribute('value') + '"')

			if expectedValues['stable'] == 'no' and not self.stable_no_input.get_attribute('checked'):
				failures.append('MyelDiagForm: Expecting "no" to having stable myeloma')
			if expectedValues['stable'] == 'yes' and not self.stable_yes_input.get_attribute('checked'):
				failures.append('MyelDiagForm: Expecting "yes" to having stable myeloma')
			if expectedValues['stable'] == 'I dont know' and not self.stable_idk_input.get_attribute('checked'):
				failures.append('MyelDiagForm: Expecting "I dont know" to having stable myeloma')

			if expectedValues['m_protein'] == 'no' and not self.mprotein_no_input.get_attribute('checked'):
				failures.append('MyelDiagForm: Expecting "no" to relapsing')
			if expectedValues['m_protein'] == 'yes' and not self.mprotein_yes_input.get_attribute('checked'):
				failures.append('MyelDiagForm: Expecting "yes" to relapsing')
			if expectedValues['m_protein'] == 'I dont know' and not self.mprotein_idk_input.get_attribute('checked'):
				failures.append('MyelDiagForm: Expecting "I dont know" to relapsing')

			if expectedValues['recent_pain'] == 'no' and not self.recent_pain_no_input.get_attribute('checked'):
				failures.append('MyelDiagForm: Expecting "no" to having recent pain')
			if expectedValues['recent_pain'] == 'yes' and not self.recent_pain_yes_input.get_attribute('checked'):
				failures.append('MyelDiagForm: Expecting "yes" to having recent pain')
			if expectedValues['recent_pain'] == 'I dont know' and not self.recent_pain_idk_input.get_attribute('checked'):
				failures.append('MyelDiagForm: Expecting "I dont know" to having recent pain')

			if expectedValues['lesions'] == 'no lesions' and not self.boneLesion0_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "no lesions" to # of bone lesions')
			elif expectedValues['lesions'] == '5 or less' and not self.boneLesion1_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "5 or less" to # of bone lesions')
			elif expectedValues['lesions'] == '6 or more' and not self.boneLesion2_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "6 or more" to # of bone lesions')
			elif expectedValues['lesions'] == 'I dont know' and not self.boneLesion3_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "I dont know" to # of bone lesions')

			if expectedValues['high_risk'] == 'no' and not self.highRisk1_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: High Risk, Expecting "no"')
			elif expectedValues['high_risk'] == 'yes' and not self.highRisk2_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: High Risk, Expecting "yes"')
			elif expectedValues['high_risk'] == 'I dont know' and not self.highRisk3_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: High Risk, Expecting "I dont know"')

			if expectedValues['stem_cell'] == 'no' and not self.stemCell1_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "no" to being eligible for stem cell')
			elif expectedValues['stem_cell'] == 'yes' and not self.stemCell2_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "yes" to being eligible for stem cell')
			elif expectedValues['stem_cell'] == 'I dont know' and not self.stemCell3_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "I dont know" to being eligible for stem cell')

			if self.facility_input.get_attribute('value') != expectedValues['facility']:
				failure.append('MyelDiagForm: Expecting facility "' + expectedValues['facility'] + '", got "' + self.facility_input.get_attribute('value') + '"')
			if self.city_input.get_attribute('value') != expectedValues['city']:
				failure.append('MyelDiagForm: Expecting city "' + expectedValues['city'] + '", got "' + self.city_input.get_attribute('value') + '"')
			if self.state_input.get_attribute('value') != expectedValues['state']:
				failure.append('MyelDiagForm: Expecfting state "' + expectedValues['state'] + '", got "' + self.state_input.get_attribute('value') + '"')

			if expectedValues['additional'] == 'no' and not self.add_diagno_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "no" to an additional diagnosis')
			elif expectedValues['additional'] == 'yes' and not self.add_diagyes_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "yes" to an additional diagnosis')

			# todo: handle verifying multiple physicians
			# For multiple physicians: Need to handle fact that physicians aren't necessarily displayed in same order they were created
			if self.phys_name_input.get_attribute('value') != expectedValues['phys_name']:
				failure.append('MyelDiagForm: Expecting physician name "' + expectedValues['phys_name'] + '", got "' + self.phys_name_input.get_attribute('value') + '"')
			if self.phys_facility_input.get_attribute('value') != expectedValues['phys_facility']:
				failure.append('MyelDiagForm: Expecting physician facility "' + expectedValues['phys_facility'] + '", got "' + self.phys_facility_input.get_attribute('value') + '"')
			if self.phys_city_input.get_attribute('value') != expectedValues['phys_city']:
				failure.append('MyelDiagForm: Expecting physician city "' + expectedValues['phys_city'] + '", got "' + self.phys_city_input.get_attribute('value') + '"')
			if self.phys_state_input.get_attribute('value') != expectedValues['phys_state']:
				failure.append('MyelDiagForm: Expecting physician state "' + expectedValues['phys_state'] + '", got "' + self.phys_state_input.get_attribute('value') + '"')

		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load MyelomaDiagnosisFreshForm')

	def load_physicians(self):
		self.physician_cont = self.driver.find_element_by_id('physician_container')
		self.physician_rows = self.physician_cont.find_elements_by_class_name('form-group')

		button_cont = self.physician_cont.find_element_by_class_name('addDiagnoisisButton')
		self.add_physician_button = button_cont.find_element_by_tag_name('i')
		self.physicians = []
		for i, physician in enumerate(self.physician_rows):
			# name, facility, city, state
			name_cont = physician.find_element_by_id('physician_name_' + str(i))
			name_inputs = name_cont.find_elements_by_tag_name('input')
			name_input = name_inputs[0]
			name_hidden_input = name_inputs[1]
			facility_input = physician.find_element_by_id('facility_name_' + str(i))

			city_input = physician.find_element_by_id('city_' + str(i))
			# State selector element depends on if state has been set already
			state_cont = physician.find_element_by_id('state' + str(i))
			state_selector = None
			state_value = ''
			try:
				value_el = state_cont.find_element_by_class_name('Select-value')
				state_value = value_el.text
				state_selector = value_el
			except NoSuchElementException:
				state_selector = state_cont.find_element_by_class_name('Select-placeholder')
			# first physician won't have delete button
			try:
				delete_button = physician.find_element_by_class_name('delete_physician_icon')
			except NoSuchElementException:
				delete_button = None
			physician = {
				'name': name_input.get_attribute('value'),
				'facility': facility_input.get_attribute('value'),
				'city': city_input.get_attribute('value'),
				'state': state_value,
				'elements': {
					'name_input': name_input,
					'name_hidden_input': name_hidden_input,
					'facility_input': facility_input,
					'city_input': city_input,
					'state_selector': state_selector,
					'delete_button': delete_button,
				}
			}
			self.physicians.append(physician)

	def load_additional_diagnoses(self):
		additional_diagnoses = []
		conts = self.driver.find_element_by_tag_name('diagnose-thrd-sec')
		for i, cont in enumerate(conts):
			dateEl = cont.find_element_by_id('diagnosisDate_' + str(i))
			dateInput = dateEl.find_element_by_tag_name('input')
			date = dateInput.get_attribute('value')

			additional_diagnoses.append({
				'date': date,
				'type': diagnosis_type
			})

		return additional_diagnoses

############################### Dropdown functions #####################################

	def load_first_diagnosis_dropdown(self):
		self.first_diagnosis_cont = self.driver.find_elements_by_class_name('frst-diag-name')[0]

		# Is value already set? Should have either value or placeholder element
		self.first_diagnosis_preSet = False
		try:
			self.firstDiagnosis_value = self.first_diagnosis_cont.find_element_by_class_name('Select-value-label')
			self.firstDiagnosis_placeholder = None
			self.first_diagnosis_preSet = True
		except NoSuchElementException:
			self.firstDiagnosis_value = None
			# 'Select diagnosis' placeholder
			self.firstDiagnosis_placeholder = self.first_diagnosis_cont.find_element_by_class_name('Select-placeholder')

	def set_first_diagnosis(self, value):
		# Click value div if already set. Placeholder if not set
		if self.first_diagnosis_preSet:
			self.firstDiagnosis_value.click()
		else:
			self.firstDiagnosis_placeholder.click()

		# Load dropdown options
		options = {}
		try:
			menu = self.form.find_element_by_class_name('Select-menu-outer')
			divs = menu.find_elements_by_tag_name('div')
			for i, div in enumerate(divs):
				if i != 0: # First div is container
					options[div.text.lower()] = divs[i]
		except NoSuchElementException:
			print('Unable to find dropdown items for first diagnosis')

		try: # click one that matches value
			option = options[value.lower()]
			option.click()
		except IndexError:
			print('invalid index: ' + value)
		WDW(self.driver, 5).until(lambda x: self.load())

	def load_facility_state(self):
		# Each state dropdown should have this class. Facility state should always be 1st
		conts = self.form.find_elements_by_class_name('state-font-custom')
		facility_cont = conts[0]

		# Is value already set? Should have either value (set) or placeholder (not set) element
		self.facility_state_preSet = False
		try:
			self.facility_state_value = facility_cont.find_element_by_class_name('Select-value-label')
			self.facility_state_placeholder = None
			self.facility_state_preSet = True
		except NoSuchElementException:
			self.facility_state_value = None
			 # 'Select state' placeholder
			self.facility_state_placeholder = facility_cont.find_element_by_class_name('Select-placeholder')

	def set_facility_state(self, value):
		# Click value div if already set. Placeholder if not set
		if self.facility_state_preSet:
			self.facility_state_value.click()
		else:
			self.facility_state_placeholder.click()

		# Load dropdown options
		dropdownOptions = {}
		try:
			menu = self.form.find_element_by_class_name('Select-menu-outer')
			divs = menu.find_elements_by_tag_name('div')
			for i, div in enumerate(divs):
				if i != 0: # First div is container
					dropdownOptions[div.text.lower()] = divs[i]
		except NoSuchElementException:
			print('Unable to find dropdown items for facility state')

		try: # click one that matches value
			option = dropdownOptions[value.lower()]
			option.click()
		except IndexError:
			print('invalid state: ' + value)
		WDW(self.driver, 5).until(lambda x: self.load())

	def set_physician_state(self, value, physicianIndex=0):
		# Click state_selector to open dropdown menu
		physician = self.physicians[physicianIndex]
		physician['elements']['state_selector'].click()

		# Load dropdown options
		dropdownOptions = {}
		try:
			menu = self.physician_rows[physicianIndex].find_element_by_class_name('Select-menu-outer')
			divs = menu.find_elements_by_tag_name('div')
			for i, div in enumerate(divs):
				if i != 0: # First div is container
					dropdownOptions[div.text.lower()] = divs[i]
		except NoSuchElementException:
			print('Unable to find dropdown items for physician ' + str(physicianIndex) + ' state')

		try: # click one that matches value
			option = dropdownOptions[value.lower()]
			option.click()
		except IndexError:
			print('invalid state: ' + value)
		# reload page to update physician values
		WDW(self.driver, 5).until(lambda x: self.load())

	def set_physician(self, physicianInfo, index):
		p_elements = self.physicians[index]['elements']
		if physicianInfo['name']:
			p_elements['name_input'].click()
			AC(self.driver).send_keys(physicianInfo['name']).perform()

		p_elements['facility_input'].clear()
		if physicianInfo['facility']:
			p_elements['facility_input'].send_keys(physicianInfo['facility'])

		p_elements['city_input'].clear()
		if physicianInfo['city']:
			p_elements['city_input'].send_keys(physicianInfo['city'])

		if physicianInfo['state']:
			self.set_physician_state(physicianInfo['state'], index)

############################## Typeahead functions ############################

	# 'name': name_input.get_attribute('value'),
	# 'facility': facility_input.get_attribute('value'),
	# 'city': city_input.get_attribute('value'),
	# 'state': state_value,
	# 'elements': {
	# 	'name_input': name_input,
	# 	'name_hidden_input': name_hidden_input,
	# 	'facility_input': facility_input,
	# 	'city_input': city_input,
	# 	'state_selector': state_selector,
	# 	'delete_button': delete_button,
	# }

	def add_physician_typeahead(self, partial_name, full_name, physicianInfo, physicianPosition):

		physician_elements = self.physicians[-1]['elements']

		physician_elements['name_input'].click()
		AC(self.driver).send_keys(partial_name).perform()

		# Wait for options to show up, then click option that matches full_name
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'rbt-menu')))

		count = 0
		loaded = False
		while not loaded or count > 10:
			count += 1
			try:
				menu = self.driver.find_element_by_class_name('rbt-menu')
				options = menu.find_elements_by_tag_name('li')
				for option in options:
					option_text = option.text
					if option_text == 'No matches found.':
						time.sleep(.5)
						break
					elif option.text == full_name:
						anchor = option.find_element_by_tag_name('a')
						anchor.click()
						loaded = True
			except StaleElementReferenceException:
				pass

	def clear_physician(self, index):
		cont = self.physician_rows[-1]
		physician_elements = self.physicians[-1]['elements']

		clear_physician_info_button = cont.find_element_by_class_name('rbt-close')
		clear_phy

	def load_state(self, expectedState=None):
		try:
			el = self.driver.find_element_by_id('stablehighRisk1')
			self.state = 'new_diagnosis'
		except NoSuchElementException:
			self.state = 'old_diagnosis'





############################## Error handling #################################

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

############################## Test functions ##################################

	def submit(self, formInfo, submit=True):
		if formInfo:
			# if formInfo['newly_diagnosed'] is not None:
			# 	if formInfo['newly_diagnosed'] == 'yes':
			# 		self.newlyDiagnosedYes_radio.click()
			# 	else:
			# 		self.newlyDiagnosedNo_radio.click()

			if formInfo['diagnosis_date'] is not None:
				picker = datePicker.DatePicker(self.driver)
				# self.dateDiagnosis_input.click()
				# picker.set_date(formInfo['diagnosis_date'], self.dateDiagnosis_input)
				dateSet = False
				while not dateSet:
					try:
						self.dateDiagnosis_input.click()
						picker.set_date(formInfo['diagnosis_date'])
						dateSet = True
					except (ElementNotVisibleException, StaleElementReferenceException, ValueError, KeyError) as e:
						print('Failed to set date. Page probably reloaded')
						time.sleep(.4)
				self.load()
				raw_input('done reloading after setting the date')

			raw_input('setting type')
			if formInfo['type'] is not None:
				self.set_first_diagnosis(formInfo['type'])

			raw_input('setting new diagnosis')
			if formInfo['stable'] is not None and self.state == 'new_diagnosis':
				stable_myeloma = formInfo['stable']
				raw_input('submit problem?')
				if stable_myeloma == 'no':
					self.stable_no_input.click()
				elif stable_myeloma == 'yes':
					self.stable_yes_input.click()
				else:
					self.stable_idk_input.click()

			raw_input('setting protein')
			if formInfo['m_protein'] is not None and self.state == 'new_diagnosis':
				stable_myeloma = formInfo['m_protein']
				if stable_myeloma == 'no':
					self.mprotein_no_input.click()
				elif stable_myeloma == 'yes':
					self.mprotein_yes_input.click()
				else:
					self.mprotein__idk_input.click()

			if formInfo['recent_pain'] is not None and self.state == 'new_diagnosis':
				stable_myeloma = formInfo['recent_pain']
				if stable_myeloma == 'no':
					self.recent_pain_no_input.click()
				elif stable_myeloma == 'yes':
					self.recent_pain_yes_input.click()
				else:
					self.recent_pain__idk_input.click()

			if formInfo['lesions'] is not None:
				bone_lesions = formInfo['lesions']
				if bone_lesions == 'no lesions':
					self.boneLesion0_radio.click()
				elif bone_lesions == '5 or less':
					self.boneLesion1_radio.click()
				elif bone_lesions == '6 or more':
					self.boneLesion2_radio.click()
				else:
					self.boneLesion3_radio.click()

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

			if formInfo['diagnosis_location']: # Empty dict should evaluate to False
				location = formInfo['diagnosis_location']
				if location['facility']:
					self.facility_input.clear()
					self.facility_input.send_keys(location['facility'])
				if location['city']:
					self.facility_city_input.clear()
					self.facility_city_input.send_keys(location['city'])
				if location['state']:
					self.set_facility_state(location['state'])

			if formInfo['additional_diagnosis'] is not None:
				add_diag = formInfo['additional_diagnosis']
				if not add_diag:
					self.add_diagNo_radio.click()
				else:
					self.add_diagYes_radio.click()
					# todo: function to load
					self.load_additional_diagnoses()
					if formInfo['additional_diagnoses']:
						pass
						# todo: recursive function: check for errors, load new inputs, check for additional_diagnoses, enter data

			if formInfo['physicians']:
				# todo: handle multiple physician inputs. load into list
				# todo: handle adding multiple physicians
				for i, physician in enumerate(formInfo['physicians']):
					# print('i: ' + str(i))
					# print('# physician inputs: ' + str(len(self.physicians)))
					if i >= len(self.physicians):
						# Form doesn't have enough rows. Add physician row and reload page
						# raw_input('adding physician')
						self.add_physician_button.click()
						WDW(self.driver, 5).until(lambda x: self.load())
						# print(str(len(self.physicians)))
						# raw_input('right # physicians?')
					# enter formInfo into last row of physician inputs
					self.set_physician(physician, i)

			if submit:
				self.continue_button.click()

			return True
		return False


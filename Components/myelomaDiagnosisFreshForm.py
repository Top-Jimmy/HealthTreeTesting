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
		# self.placeholders = self.form.find_elements_by_class_name('Select-placeholder')

		self.newlyDiagnosedNo_radio = self.form.find_element_by_id('newly_diagnosedNo')
		self.newlyDiagnosedYes_radio = self.form.find_element_by_id('newly_diagnosedYes')

		self.dateDiagnosis_cont = self.form.find_element_by_class_name('mnth-datepicker')
		self.dateDiagnosis_input = self.dateDiagnosis_cont.find_element_by_tag_name('input')

		self.load_first_diagnosis_dropdown()
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

		# todo: handle loading state dropdown based on whether first diagnosis is preSet
		self.facility_input = self.form.find_element_by_id('facility_name')
		self.facility_city_input = self.form.find_element_by_id('Last')
		self.load_facility_state()

		self.add_diagNo_radio = self.form.find_element_by_id('yesno0')
		self.add_diagYes_radio = self.form.find_element_by_id('yesno1')

		# todo handle loading multiple diagnosis inputs, delete diagnosis button, add diagnosis action

		self.load_physicians()

		button_cont = self.form.find_element_by_class_name('submit_button')
		self.continue_button = button_cont.find_element_by_tag_name('button')

		# self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
		if expectedValues:
			if expectedValues['newly_diagnosed'] == 'no' and not self.newly_diagnosedNo_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "no" to being newly diagnosed')
			elif expectedValues['newly_diagnosed'] == 'yes' and not self.newly_diagnosedYes_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "yes" to being newly diagnosed')

			if self.dateDiagnosis_form-control.get_attribute('value') != expectedValues['date']:
				failures.append('MyelDiagForm: Expecting date of diagnosis "' + expectedValues['date'] + '", got "' + self.dateDiagnosis_form-control.get_attribute('value') + '"')

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
			elif expectedValues['additional'] == 'yes' and not self.add_diagyes_radio.get_attribute('checked'):
				failure.append('MyelDiagForm: Expecting "yes" to an additional diagnosis')

			# todo: handle verifying multiple physicians
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
		# todo: need id for physician container
			# keep track of # of physicians
			# loop through and find (name, facility, city, state)
				# for physicians after the first, load delete button
			# find 'add physician' button
			# put all physicians in object? Maybe not necessary if we're keeping track of # of physicians


		# First physician: Name, Facility, City, State
		self.phys_name_cont = self.form.find_element_by_class_name('rbt-input-hint-container')
		phys_inputs = self.phys_name_cont.find_elements_by_tag_name('input')
		self.phys_name_input = self.form.find_element_by_id('physician_name_0')
		self.phys_name_hiddenInput = phys_inputs[1]

		cont = self.form.find_element_by_id('facility_name_0')
		self.phys_facility_input = cont.find_element_by_tag_name('input')

		cont = self.form.find_element_by_id('city0')
		self.phys_city_input = cont.find_element_by_tag_name('input')

		self.load_physician_state(0)




		# physicians = []

		# physician_cont = self.form.find_element_by_class_name('??')
		# rows = physician_cont.find_elements_by_class_name('form-group')
		# for i, row in enumerate(rows):
		# 	inputs = row.find_element_by_tag_name('input')

		# 	try:
		# 		el = row.find_element_by_class_name('Select-value')
		# 		state = el.text
		# 	except NoSuchElementException:
		# 		state = None

		# 	try:
		# 		delete_name_button = row.find_element_by_class_name('rbt-close')
		# 	except NoSuchElementException:
		# 		delete_name_button = None

		# 	try:
		# 		delete_physician_button = row.find_element_by_class_name('delete_physician_icon')
		# 	except NoSuchElementException:
		# 		delete_physician_button = None



		# 	physician = {
		# 		'name': inputs[0].text,
		# 		'facility': inputs[2].text,
		# 		'city': inputs[3].text,
		# 		'state': state,

		# 		'delete_name_button': delete_button,
		# 		'delete_physician_button': delete_physician_button,
		# 	}

		# 	physicians.append(physician)

		# 	return physicians


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
		self.first_diagnosis_cont = self.driver.find_elements_by_class_name('frst-diag-name')[1]

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
		conts = self.form.find_elements_by_class_name('state-font-custom')
		facility_cont = conts[0]

		# Is value already set? Should have either value or placeholder element
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

	def load_physician_state(self, physicianIndex):
		# todo: don't assign to variables. Put into object (needs to handle n physicians)
		cont = self.form.find_element_by_id('state' + str(physicianIndex))

		# Is value already set? Should have either value or placeholder element
		self.physician_state_preSet = False
		try:
			self.physician_state_value = cont.find_element_by_class_name('Select-value')
			self.physician_state_placeholder = None
			self.physician_state_preSet = True
		except NoSuchElementException:
			self.physician_state_value = None
			 # 'Select state' placeholder
			self.physician_state_placeholder = cont.find_element_by_class_name('Select-placeholder')

	def set_physician_state(self, value, physicianIndex=0):
		# todo: handle grabbing right physician object, instead of static variables

		# Click value div if already set. Placeholder if not set
		if self.physician_state_preSet:
			self.physician_state_value.click()
		else:
			self.physician_state_placeholder.click()

		# Load dropdown options
		dropdownOptions = {}
		try:
			menu = self.form.find_element_by_class_name('Select-menu-outer')
			divs = menu.find_elements_by_tag_name('div')
			for i, div in enumerate(divs):
				if i != 0: # First div is container
					dropdownOptions[div.text.lower()] = divs[i]
		except NoSuchElementException:
			print('Unable to find dropdown items for physician state')

		try: # click one that matches value
			option = dropdownOptions[value.lower()]
			option.click()
		except IndexError:
			print('invalid state: ' + value)
		WDW(self.driver, 5).until(lambda x: self.load())

############################## Typeahead functions ############################

	def add_physician_typeahead(self, partial_name, full_name, physicianInfo):
		# todo: needs to be able to add a new physician

		self.phys_name_input.click()
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

		# todo: need to verify physicianInfo matches data loaded for last physician

		# Verify physicianInfo
		# self.load('fresh', physicianInfo)

	# def clear_physician(self, physicianIndex=0):
		# Use typeahead


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
			if formInfo['newly_diagnosed'] is not None:
				if formInfo['newly_diagnosed']:
					self.newlyDiagnosedYes_radio.click()
				else:
					self.newlyDiagnosedNo_radio.click()

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
					except (ElementNotVisibleException, StaleElementReferenceException) as e:
						print('Failed to set date. Page probably reloaded')
						time.sleep(.4)

			if formInfo['type'] is not None:
				self.set_first_diagnosis(formInfo['type'])

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
						self.set_physician_state(physician['state'])

			if submit:
				self.continue_button.click()
			return True
		return False

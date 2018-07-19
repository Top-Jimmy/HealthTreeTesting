import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException, WebDriverException)
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
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.form = self.driver.find_element_by_id('diagnosis_form')
		self.rows = self.form.find_elements_by_class_name('form-group')
		self.load_state()
		print(self.state)

		# self.dateDiagnosis_cont = self.form.find_element_by_class_name('mnth-datepicker')
		# self.dateDiagnosis_input = self.rows[0].find_element_by_tag_name('input')
		self.load_first_diagnosis_dropdown()

		if self.state == 'extra_questions':
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

		self.highRisk_tooltip = self.form.find_element_by_class_name('tool-tip-history')
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

		self.load_additional_diagnoses()
		self.load_physicians()
		button_cont = self.form.find_element_by_class_name('submit_button')
		self.continue_button = button_cont.find_element_by_tag_name('button')

		return self.validate(expectedValues)

	def validate(self, expectedValues):
		failures = []
		if expectedValues:

			# meta validation
			try:
				meta = expectedValues['meta']
				numAddDiagnoses = meta.get('numAddDiagnoses', None)
				if numAddDiagnoses and numAddDiagnoses != len(self.additional_diagnoses):
					failures.append('MyelDiagFreshForm Meta: Expected ' + str(numAddDiagnoses) + ' additional Diagnoses. Form loaded ' + str(len(self.additional_diagnoses)))

				numRows = meta.get('numRows', None)
				if numRows and numRows != len(self.rows):
					failures.append('MyelDiagFreshForm Meta: Expected ' + str(numRows) + ' additional Diagnoses. Form loaded ' + str(len(self.rows)))
				# for key, value in meta_validators:
				# 	print('key: ' + str(key))
				# 	print('value: ' + str(value))
					# for key, value in validator.iteritems():
					# 	if key == 'numAddDiagnoses' and value != len(self.additional_diagnoses):


					# 	if key == 'numRows' and value != len(self.rows):

			except KeyError:
				# No meta validation
				print('no meta')
				pass

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

		return True

		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load MyelomaDiagnosisFreshForm')

	def expectedNumRows(self):
		# default
		expectedRows = 9

		# 3 extra questions for old diagnosis (> 1 year ago)
		if ('M-protein' in self.driver.page_source):
			expectedRows += 3

		# any additional diagnoses? 4 rows each
		if len(self.additional_diagnoses) > 0:
			adding = 4*len(self.additional_diagnoses)
			expectedRows += adding

		return expectedRows

	def load_physicians(self):
		self.physician_cont = self.driver.find_element_by_id('physician_container')
		self.physician_rows = self.physician_cont.find_elements_by_class_name('form-group')

		button_cont = self.physician_cont.find_element_by_class_name('addDiagnoisisButton')
		self.add_physician_button = button_cont.find_element_by_tag_name('i')
		self.physicians = []
		for i, physician in enumerate(self.physician_rows):
			# name, facility, city, state
			name_cont = physician.find_element_by_id('physician_diagnostician_' + str(i))
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
		conts = self.driver.find_elements_by_class_name('diagnose-thrd-sec')
		for containerIndex, cont in enumerate(conts):
			dateInput = cont.find_element_by_id('diagnosisDate_' + str(containerIndex + 1))
			date = dateInput.get_attribute('value')
			diagnosisBox = cont.find_element_by_id('next_diag_type_' + str(containerIndex + 1))
			diagnosisInput = diagnosisBox.find_element_by_tag_name('input')
			diagnosis_type = diagnosisInput.get_attribute('value')

			boneRadios = []
			try:
				boneRadios.append(cont.find_element_by_id(str(containerIndex+1) + 'add_bone0'))
				boneRadios.append(cont.find_element_by_id(str(containerIndex+1) + 'add_bone1'))
				boneRadios.append(cont.find_element_by_id(str(containerIndex+1) + 'add_bone2'))
				boneRadios.append(cont.find_element_by_id(str(containerIndex+1) + 'add_bone3'))
			except NoSuchElementException:
				print('Failed to find additional diagnosis bone lesion radio buttons')

			# which is selected?
			options = ['no lesions', '5 or more lesions', '6 or more lesions', 'I dont know']
			bone_lesions = None
			for i, radio in enumerate(boneRadios):
				if radio.is_selected():
					bone_lesions = options[i]

			additional_diagnoses.append({
				'date': date,
				# 'dateInput': dateInput,
				'type': diagnosis_type,
				# 'typeEl': typeEl,
				'lesions': bone_lesions,
				# 'bone_lesions_cont': bone_lesions_cont,
				'index': containerIndex,
			})

		self.additional_diagnoses = additional_diagnoses

		# Add button
		buttons = self.driver.find_elements_by_class_name('addDiagnoisisButton')
		if len(buttons) > 1:
			# Always get add physician, only get add diagnosis when question is answered yes
			self.add_diagnosis_button = buttons[0]

############################### Dropdown functions #####################################

	def set_dropdown(self, cont, value):
		# find right container given index (class='Select-control')
		# conts = self.driver.find_elements_by_class_name('Select-control')
		# cont = conts[dropdownIndex]

		# Figure out if you need to click 'Select-value-label' or 'Select-placeholder' element
		dropdown_preSet = False
		try:
			dropdown_value = cont.find_element_by_class_name('Select-value-label')
			dropdown_placeholder = None
			dropdown_preSet = True
		except NoSuchElementException:
			dropdown_value = None
			dropdown_placeholder = cont.find_element_by_class_name('Select-placeholder')

		# click it
		if dropdown_preSet:
			dropdown_value.click()
		else:
			dropdown_placeholder.click()
		# load options in dropdown
		options = {}
		try:
			menu = self.form.find_element_by_class_name('Select-menu-outer')
			divs = menu.find_elements_by_tag_name('div')
			for i, div in enumerate(divs):
				if i != 0:
					options[div.text.lower()] = divs[i]
		except NoSuchElementException:
			print('Unable to find dropdown items for first diagnosis')

		# click option
		try:
			option = options[value.lower()]
			option.click()

		except (IndexError, KeyError) as e:
			print('invalid index: ' + value)
			for option in options:
				print(option)

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
		count = 0
		loaded = False
		while not loaded and count < 5:
		  try:
			menu = self.physician_rows[physicianIndex].find_element_by_class_name('Select-menu-outer')
			divs = menu.find_elements_by_tag_name('div')
			for i, div in enumerate(divs):
			  if i != 0: # First div is container
				dropdownOptions[div.text.lower()] = divs[i]
			loaded = True
		  except NoSuchElementException:
			print('Unable to find states in physician dropdown')
			count += 1

		# try:
		# 	menu = self.physician_rows[physicianIndex].find_element_by_class_name('Select-menu-outer')
		# 	divs = menu.find_elements_by_tag_name('div')
		# 	for i, div in enumerate(divs):
		# 		if i != 0: # First div is container
		# 			dropdownOptions[div.text.lower()] = divs[i]
		# except NoSuchElementException:
		# 	print('Unable to find dropdown items for physician ' + str(physicianIndex) + ' state')

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

	def add_physician_typeahead(self, partial_name, full_name, physicianInfo):
		# Enter partial_name, select option w/ full_name, verify info matches physicianInfo

		# Enter partial_name
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

		# Reload to avoid staleElementException
		WDW(self.driver, 10).until(lambda x: self.load())
		physician_elements = self.physicians[-1]['elements']

		# Validate physicianInfo
		failures = []
		if physicianInfo['name'] != physician_elements['name_input'].get_attribute('value'):
			failures.append('Name does not match.')
		if physicianInfo['facility'] != physician_elements['facility_input'].get_attribute('value'):
			failures.append('Facility does not match')
		if physicianInfo['city'] != physician_elements['city_input'].get_attribute('value'):
			failures.append('City does not match')
		if physicianInfo['state'] != physician_elements['state_selector'].text:
			failures.append('State does not match')

		if len(failures) > 0:
			for failure in failures:
				print(failure)
			return False
		else:
			return True

	def clear_physician(self, index):
		cont = self.physician_rows[-1]
		physician_elements = self.physicians[-1]['elements']

		clear_physician_info_button = cont.find_element_by_class_name('rbt-close')
		clear_phy

	def load_state(self, expectedState=None):
		# Should have 3 extra questions when...
		# 1. Diagnosis date is > 1 year ago
		# 2. AND correct diagnosis type is selected (i.e. not first 2 options, MGUS or smoldering)
		try:
			el = self.driver.find_element_by_id('stablehighRisk1')
			self.state = 'extra_questions'
		except NoSuchElementException:
			self.state = 'default'


############################## Test functions ##################################

	def submit(self, formInfo, submit=True):
		if formInfo:
			if formInfo['diagnosis_date'] is not None:
				picker = datePicker.DatePicker(self.driver, self.rows[0])
				dateSet = False
				while not dateSet:
					try:
						# self.dateDiagnosis_input.click()
						picker.set_date(formInfo['diagnosis_date'])
						dateSet = True
					except (ElementNotVisibleException, StaleElementReferenceException, ValueError, KeyError, AttributeError, WebDriverException) as e:
						print('Failed to set date. Page probably reloaded')
						time.sleep(.4)
				self.load()

			if formInfo['type'] is not None:
				self.set_dropdown(self.rows[1], formInfo['type'])

			# Update state (might have 3 new questions)
			self.load_state()
			if self.state == 'extra_questions':
				self.load()

			if formInfo['stable'] is not None and self.state == 'extra_questions':
				stable_myeloma = formInfo['stable']
				if stable_myeloma == 'no':
					self.stable_no_input.click()
				elif stable_myeloma == 'yes':
					self.stable_yes_input.click()
				else:
					self.stable_idk_input.click()

			if formInfo['m_protein'] is not None and self.state == 'extra_questions':
				stable_myeloma = formInfo['m_protein']
				if stable_myeloma == 'no':
					self.mprotein_no_input.click()
				elif stable_myeloma == 'yes':
					self.mprotein_yes_input.click()
				else:
					self.mprotein__idk_input.click()

			if formInfo['recent_pain'] is not None and self.state == 'extra_questions':
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
					expectedRows = self.expectedNumRows() + 4 # expected + 4 for new diagnosis
					expectedValues = {
						'meta': {
							'numAddDiagnoses': 1,
							'numRows': expectedRows,
						}
					}
					WDW(self.driver, 5).until(lambda x: self.load(expectedValues))
					self.add_diagnoses(formInfo['additional_diagnoses'])

			if formInfo['physicians']:
				# todo: handle multiple physician inputs. load into list
				# todo: handle adding multiple physicians
				for i, physician in enumerate(formInfo['physicians']):
					# print('i: ' + str(i))
					# print('# physician inputs: ' + str(len(self.physicians)))
					if i >= len(self.physicians):
						# Form doesn't have enough rows. Add physician row and reload page
						self.add_physician_button.click()
						WDW(self.driver, 5).until(lambda x: self.load())
					# enter formInfo into last row of physician inputs
					self.set_physician(physician, i)

			if submit:
				self.continue_button.click()

			return True
		return False

	def add_diagnoses(self, additional_diagnoses):
		# Calculate row of 1st additional diagnosis diagnosis date (used as container for datePicker)
		# Depends on if 3 'old' questions are showing
		rowIndex = 7
		if self.state == 'extra_questions':
			rowIndex = 10

		# For each diagnosis, (1) set date, (2) set type, (3) set lesions, (4) click add button (if adding more)
		for i, diagnosis in enumerate(additional_diagnoses):
			conts = self.driver.find_elements_by_class_name('diagnose-thrd-sec')
			cont = conts[i]

			# set date
			# dateInput = cont.find_element_by_id('diagnosisDate_' + str(i + 1))
			picker = datePicker.DatePicker(self.driver, self.rows[rowIndex])
			dateSet = False
			while not dateSet:
				try:
					# dateInput.click()
					picker.set_date(diagnosis['date'])
					dateSet = True
				except ElementNotVisibleException:
					print('notVisible')
				except StaleElementReferenceException:
					print('stale')
				except ValueError:
					print('value')
				except KeyError:
					print('key')
				except(AttributeError):
					print('attribute')
				except WebDriverException:
					print('Failed to set date. Page probably reloaded')
				time.sleep(.4)

			# set diagnosis type
			if diagnosis['type']:
				# Row right after date row index
				self.set_dropdown(self.rows[rowIndex+1], diagnosis['type'])

			# set lesions
			if diagnosis['lesions']:
				# get index of radio button given value
				options = ['no lesions', '5 or more lesions', '6 or more lesions', 'i dont know']
				try:
					optionIndex = options.index(diagnosis['lesions'].lower())
				except KeyError:
					raw_input('Setting additional diagnosis lesions: bad key! ' + str(diagnosis['lesions'].lower()))

				# Get radio input
				try:
					radioId = str(i+1) + 'add_bone' + str(optionIndex)
					radioInput = cont.find_element_by_id(radioId)
					radioInput.click()
				except NoSuchElementException:
					raw_input('Setting additional diagnosis lesions: bad radio id! ' + str(radioId))

			# update row index
			rowIndex += 4 # 3 rows for date, type and bone lesions. 1 for add button (even if it doesn't have add button)

			# Click add diagnosis button (if necessary)
			if i + 1 < len(additional_diagnoses):
				self.add_diagnosis_button.click()
				# Wait until first additional diagnosis has loaded (make sure right # of rows is added)
				expectedRows = self.expectedNumRows() + 4 # expected + 4 for new diagnosis
				expectedValues = {
					'meta': {
						'numAddDiagnoses': 1,
						'numRows': expectedRows,
					}
				}
				WDW(self.driver, 5).until(lambda x: self.load(expectedValues))
				# print('2. has # rows: ' + str(expectedRows))

	def cancel_physician(self, physicianInfo):
		self.set_physician(physicianInfo, 0)

		self.add_physician_button.click()
		self.delete_button = self.form.find_element_by_class_name('delete_physician_icon')
		self.delete_button.click()

	def tooltip(self):
		self.highRisk_tooltip.click()
		p = self.form.find_element_by_class_name('tooltip-p')
		if p.text != 'Risk in myeloma is tied to disease stage, chromosomal abnormalities, disease biology, and gene expression. In the Myeloma Genetics page we will gather more details about risk.':
			print('tooltip not clicked correctly: ' + str(p.text))
			return False
		return True


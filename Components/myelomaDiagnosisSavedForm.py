import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datePicker
import popUpForm # Popup for deleting diagosis or physician
import editDiagnosisForm
import additionalDiagnosisForm
import addPhysicianForm

# Form on 'Myeloma Diagnosis' displaying user's saved diagnosis info

class MyelomaDiagnosisSavedForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues):
		self.form = self.driver.find_element_by_id('diagnosis_form')
		add_buttons = self.form.find_elements_by_class_name('custom_addDiagnoisisButton')

		self.diagnosis_tables = self.form.find_elements_by_class_name('diagnosis-frst-table')
		self.diagnoses = self.load_diagnoses()
		self.add_diagnosis_button = add_buttons[0].find_element_by_tag_name('p')

		self.physician_tables = self.form.find_elements_by_class_name('diagnosis-scnd-table')
		self.physicians = self.load_physicians()
		self.add_physician_button = add_buttons[1].find_element_by_tag_name('div')

		cont = self.form.find_element_by_class_name('submit_button')
		self.continue_button = cont.find_element_by_tag_name('button')

		self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		if expectedValues:
			failures = []

			# meta validation
			try:
				meta_validators = expectedValues['meta']
				for validator in meta_validators:
					for key, value in validator.iteritems():
						if key == 'num_diagnoses' and value != len(self.diagnoses):
							failures.append('MyelDiagSavedForm Meta: Expected ' + str(value) + ' diagnoses. Form has ' + str(len(self.diagnoses)))
						elif key == 'num_physicians' and value != len(self.physicians):
							failures.append('MyelomaDiagnosisSavedForm Meta: Expected ' + str(value) + ' physicians. Form has ' + str(len(self.physicians)))
			except KeyError:
				pass

			# Only perform form validation if 'whole' formData dictionary is passed in
			try:
				# Should only have 'diagnosis_date' if whole dictionary passed in
				test = expectedValues['diagnosis_date']

				expectedDiagnoses = self.convert_expected_diagnoses(expectedValues)
				expectedPhysicians = expectedValues['physicians']

				# Right # of diagnoses and physicians?
				if len(expectedDiagnoses) != len(self.diagnoses):
					failures.append('MyelDiagSavedForm: Expected ' + str(len(expectedDiagnoses)) + ' diagnoses. Form has ' + str(len(self.diagnoses)))
				if len(expectedValues['physicians']) != len(self.physicians):
					failures.append('MyelDiagSavedForm: Expected ' + str(len(expectedPhysicians)) + ' physicians. Form has ' + str(len(self.physicians)))

				# Diagnoses match expected values?
				keys = ['date', 'type', 'lesions', 'facility', 'city', 'state']
				for i, diagnosis in enumerate(self.diagnoses):
					for key in keys:
						if key in expectedDiagnoses and diagnosis[key] != expectedDiagnoses[key]:
							failures.append('MyelDiagForm: Diagnosis ' + str(i) + ' expected "' + key + '" ' + expectedDiagnoses[key]
								+ '", got ' + diagnoses[key])

				# Physicians match expected values?
				physician_keys = ['name', 'facility', 'city', 'state']
				for i, physician in enumerate(self.physicians):
					print(i)
					for p_key in physician_keys:
						print(p_key)
						if p_key in expectedPhysicians and physician[p_key] != expectedPhysicians[p_key]:
							failures.append('MyelDiagForm: Physican ' + str(i) + ' expected "' + p_key + '" ' + expectedPhysicians[key]
								+ '", got ' + physician[key])
			except KeyError:
				pass

			if len(failures) > 0:
				for failure in failures:
					print(failure)
				raise NoSuchElementException('Failed to load MyelomaDiagnosisSavedForm')

	def load_diagnoses(self):
		diagnoses = []
		if self.diagnosis_tables:
			for table in self.diagnosis_tables:
				# Pull info out of diagnosis table
				row = table.find_element_by_class_name('borderTableRow')
				diagnosis = {}
				values = [] # Store text in each div
				divs = row.find_elements_by_tag_name('div')
				for divIndex, div in enumerate(divs):
					if divIndex != 3: # div 3 is container div for state and city
						values.append(div.text.replace("'", '')) # Get rid of ' in "I don't know"

				# Grab text out of list
				diagnosis['date'] = self.convertDate(values[0], 'mm/yyyy')
				diagnosis['type'] = values[1]
				diagnosis['lesions'] = values[2]
				diagnosis['facility'] = values[3]

				cityState_text = values[4] # Sandy, Utah
				index = cityState_text.find(',')
				if index != -1:
					diagnosis['city'] = cityState_text[:index]
					diagnosis['state'] = cityState_text[index+2:]
				else: # Assume it's an additional diagnosis (no facility)
					diagnosis['city'] = ''
					diagnosis['state'] = ''

				# Diagnosis actions
				diagnosis['actions'] = self.load_actions(table)

				diagnoses.append(diagnosis)

				
				

		return diagnoses

	def load_actions(self, table):
		actions = {}
		actionRows = self.driver.find_elements_by_class_name('bottom-last-row')
		for i, actionRow in enumerate(actionRows):
			cont1 = actionRows[i].find_element_by_class_name('edit-treatment-icon')
			actions['edit'] = cont1.find_element_by_tag_name('a')
			cont2 = actionRows[i].find_element_by_class_name('delete-treatment-icon')
			actions['delete'] = cont2.find_element_by_tag_name('a')
		return actions
		

	def load_physicians(self):
		physicians = []
		if self.physician_tables:
			for table in self.physician_tables:
				row = table.find_element_by_class_name('borderTableRow')
				physician = {}
				values = []
				divs = row.find_elements_by_tag_name('div')
				for i, div in enumerate(divs):
					values.append(div.text)
				# Data
				physician['name'] = values[0]
				physician['facility'] = values[1]
				physician['city'] = values[2]
				physician['state'] = values[3]
				
				physician['actions'] = self.load_actions(table)

				physicians.append(physician)
		return physicians

########################### Utility Functions #############################

	def convertDate(self, dateStr, outputType='mm/yyyy'):
		if dateStr:
			months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

			if outputType == 'mm/yyyy': # Concert from 'mmm yyyy' to 'mm/yyyy'
				# dateStr = 'Jan 2000'

				index = dateStr.find(' ', None)
				if index:
					month = dateStr[:index] # 'Jan'
					try:
						monthIndex = months.index(month) + 1 # 1
					except ValueError:
						print(str(month) + ' Not in list of months')

					# add leading 0
					month = str(monthIndex).zfill(2)
					year = dateStr[index + 1:]

					return month + '/' + year
				else:
					print('mm/yyyy: Unable to convert date: ' + dateStr)
					return dateStr

			else: # Concert from 'mm/yyyy' to 'mmm yyyy'
				# dateStr = '01/2018'

				index = dateStr.find('/', None)
				if index:

					# Get month
					month = dateStr[:index] # '01'
					monthIndex = int(month) -1 # 0
					month = months[monthIndex] # 'Jan'

					year = dateStr[index + 1:]

					return month + ' ' + year
				else:
					print('mmm yyyy: Unable to convert date: ' + dateStr)
					return dateStr

	def convert_expected_diagnoses(self, expectedValues):
		# Combine 'initialDiagnosis' and 'additional_diagnoses' from expectedValues.
		# Save into object equivalent to what this form loads.
		diagnoses = []
		initialDiagnosis = {
			'date': expectedValues['diagnosis_date'],
			'type': expectedValues['type'],
			'lesions': expectedValues['lesions'],
			'facility': expectedValues['diagnosis_location']['facility'],
			'city': expectedValues['diagnosis_location']['city'],
			'state': expectedValues['diagnosis_location']['state'],
		}
		diagnoses.append(initialDiagnosis)
		# Additional diagnoses only have date and type.
		for diagnosis in expectedValues['additional_diagnoses']:
			diagType = diagnosis.get('type', None)
			date = diagnosis.get('date', None),
			lesions = diagnosis.get('lesions', None)
			additional_diagnosis = {
				'date': date,
				'type': diagType,
				'lesions': lesions,
			}
			diagnoses.append(additional_diagnosis)
		return diagnoses


########################### User Functions #############################

	def add_diagnosis(self, diagnosisInfo, action='submit'):
		self.add_diagnosis_button.click()

		self.additionalDiagnosisForm = additionalDiagnosisForm.AdditionalDiagnosisForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.additionalDiagnosisForm.load())
		self.additionalDiagnosisForm.submit(diagnosisInfo)
		# Wait for modal and loading overlay to disappear
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		return True

	def edit_diagnosis(self, diagnosisInfo, diagnosis_index=0, action='submit'):
		self.diagnoses[diagnosis_index]['edit'].click()
		time.sleep(1)
		self.editDiagnosisForm = editDiagnosisForm.EditDiagnosisForm(self.driver)
		self.editDiagnosisForm.submit(diagnosisInfo, action)
		# Wait for modal and loading overlay to disappear
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		return True

	def delete(self, del_type='diagnosis', index=0, popUpAction='confirm'):
		# Deleting physicians or diagnoses?
		dataList = self.physicians
		if del_type == 'diagnosis':
			dataList = self.diagnoses

		# deleting one or all?
		length = 1
		if index == 'all':
			length = len(dataList)

		for i in xrange(length):
			# print('deleting: ' + str(i))
			if index != 'all':
				dataList[index]['actions']['delete'].click()
			else:
				# Delete from last position to first (don't have to reload)
				delIndex = len(dataList) - (i + 1)
				raw_input('i wake up in the morning and i step outside')
				dataList[delIndex]['actions']['delete'].click()


			self.popUpForm = popUpForm.PopUpForm(self.driver)
			WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
			self.popUpForm.confirm(popUpAction)
			# Wait for confirm popup and loading overlay to disappear
			WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'react-confirm-alert')))
			WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		return True

	def add_physician(self, physicianInfo, action='submit'):
		raw_input('i said hey, whats going on?')
		self.add_physician_button.click()
		self.addPhysicianForm = addPhysicianForm.AddPhysicianForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.addPhysicianForm.load())
		self.addPhysicianForm.submit(physicianInfo, action)
		# Wait for modal and loading overlay to disappear
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		return True





import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datePicker

# Form on 'Myeloma Diagnosis' when user has already saved diagnosis info but wants to add additional diagnoses

class AdditionalDiagnosisForm():

	def __init__(self, driver):
		self.driver = driver
		# self.load(expectedValues)

	def load(self, expectedValues=None):
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

		self.cont = self.driver.find_element_by_class_name('modal-content')
		self.buttons = self.cont.find_elements_by_tag_name('button')
		self.rows = self.cont.find_elements_by_class_name('row')

		self.close_button = self.buttons[0] # x in upper right
		self.submit_button = self.buttons[1]
		self.cancel_button = self.buttons[2]

		# self.dateDiagnosis_cont = self.cont.find_element_by_class_name('mnth-datepicker')
		# self.dateDiagnosis_input = self.dateDiagnosis_cont.find_element_by_tag_name('input')

		self.lesions0 = self.cont.find_element_by_id('0')
		self.lesions1 = self.cont.find_element_by_id('1')
		self.lesions2 = self.cont.find_element_by_id('2')
		self.lesions3 = self.cont.find_element_by_id('3')

		self.load_first_diagnosis_dropdown()
		self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
		# Check # of buttons, text of buttons
		if len(self.buttons) > 3:
			failures.append('AddDiagnosisForm: Expecting 3 buttons in form. Loaded ' + str(len(self.buttons)))
		if self.submit_button.text.lower() != 'submit':
			failures.append('AddDiagnosisForm: Expecting "Submit" on button. Loaded ' + self.submit_button.text)
		if self.cancel_button.text.lower() != 'cancel':
			failures.append('AddDiagnosisForm: Expecting "Cancel" on button. Loaded ' + self.cancel_button.text)

		if len(failures) > 0:
			for failure in failures:
				print(failure)
			raise NoSuchElementException('Failed to load AdditionalDiagnosisForm')

############################### Dropdown functions #####################################

	def load_first_diagnosis_dropdown(self):
		self.first_diagnosis_cont = self.cont.find_element_by_class_name('stateFont')

		# Is value already set? Should have either value or placeholder element
		self.diagnosis_preset = False
		try:
			self.diagnosis_value = self.first_diagnosis_cont.find_element_by_class_name('Select-value-label')
			self.diagnosis_placeholder = None
			self.diagnosis_preset = True
		except NoSuchElementException:
			self.diagnosis_value = None
			# 'Select diagnosis' placeholder
			self.diagnosis_placeholder = self.first_diagnosis_cont.find_element_by_class_name('Select-placeholder')

	def set_first_diagnosis(self, value):
		# Click value div if already set. Placeholder if not set
		if self.diagnosis_preset:
			self.diagnosis_value.click()
		else:
			self.diagnosis_placeholder.click()

		# Load dropdown options
		options = {}
		try:
			menu = self.cont.find_element_by_class_name('Select-menu-outer')
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


############################## Test functions ##################################

	def submit(self, formInfo):
		if formInfo:

			# Date
			if formInfo['date'] is not None:
				picker = datePicker.DatePicker(self.driver, self.rows[0])
				dateSet = False
				while not dateSet:
					try:
						# self.dateDiagnosis_input.click()
						picker.set_date(formInfo['date'])
						dateSet = True
					except (ElementNotVisibleException, StaleElementReferenceException) as e:
						print('Failed to set date. Page probably reloaded')
						time.sleep(.4)

			# Type
			if formInfo['type'] is not None:
				self.set_first_diagnosis(formInfo['type'])

			# Bone lesions
			if formInfo['lesions'] is not None:
				bone_lesions = formInfo['lesions']
				if bone_lesions == 'no lesions':
					self.lesions0.click()
				elif bone_lesions == '5 or less':
					self.lesions1.click()
				elif bone_lesions == '6 or more':
					self.lesions2.click()
				else:
					self.lesions3.click()

			self.submit_button.click()
			return True
		return False

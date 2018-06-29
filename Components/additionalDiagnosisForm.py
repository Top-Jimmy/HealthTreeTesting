import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW
import datePicker

# Form on 'Myeloma Diagnosis' when user has already saved diagnosis info but wants to add additional diagnoses

class AdditionalDiagnosisForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues=None):
		self.cont = self.driver.find_element_by_class_name('modal-content')
		buttons = self.cont.find_elements_by_tag_name('button')
		# self.placeholders = self.form.find_elements_by_class_name('Select-placeholder')
		self.close_button = buttons[0]
		self.submit_button = buttons[1]
		self.cancel_button = buttons[2]

		self.dateDiagnosis_cont = self.cont.find_element_by_class_name('mnth-datepicker')
		self.dateDiagnosis_input = self.dateDiagnosis_cont.find_element_by_tag_name('input')

		self.load_first_diagnosis_dropdown()
		# self.validate(expectedValues)
		return True

	# def validate(self, expectedValues):
	# 	failures = []
	# 	if self.dateDiagnosis_form-control.get_attribute('value') != expectedValues['date']:
	# 		failures.append('MyelDiagForm: Expecting date of diagnosis "' + expectedValues['date'] + '", got "' + self.dateDiagnosis_form-control.get_attribute('value') + '"')

	# 	if len(failures) > 0:
	# 		print(failures)
	# 		raise NoSuchElementException('Failed to load AdditionalDiagnosisForm')

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



############################## Error handling ##################################

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

	def submit(self, formInfo):
		if formInfo:

			if formInfo['date'] is not None:
				picker = datePicker.DatePicker(self.driver, self.rows[0])
				dateSet = False
				while not dateSet:
					try:
						self.dateDiagnosis_input.click()
						picker.set_date(formInfo['date'])
						dateSet = True
					except (ElementNotVisibleException, StaleElementReferenceException) as e:
						print('Failed to set date. Page probably reloaded')
						time.sleep(.4)

			if formInfo['type'] is not None:
				self.set_first_diagnosis(formInfo['type'])

				self.submit_button.click()
			return True
		return False

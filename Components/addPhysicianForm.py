import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW

# Form on 'Myeloma Diagnosis' when user has not saved diagnosis info.

class AddPhysicianForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues=None):
		self.cont = self.driver.find_element_by_class_name('modal-content')
		buttons = self.cont.find_elements_by_tag_name('button')

		self.close_button = self.buttons[0]

		self.load_physicians()

		self.submit_button = self.buttons[1]
		self.cancel_button = self.buttons[2]

		# self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
		if expectedValues:
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
			raise NoSuchElementException('Failed to load AddPhysicianForm')

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
		# cont = self.form.find_element_by_id('state0')
		# self.phys_state_input = cont.find_element_by_tag_name('input')
		# self.phys_state_clicker = self.placeholders[2]
		# todo: load additional physician button

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
						# self.phys_state_input.clear()
						# self.phys_state_input.send_keys(physician['state'])

					self.continue_button.click()
			return True
		return False

import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW

# Form on 'Myeloma Diagnosis' when user has not saved diagnosis info.

class AddPhysicianForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.cont = self.driver.find_element_by_class_name('modal-content')
		buttons = self.cont.find_elements_by_tag_name('button')
		self.close_button = buttons[0]
		self.submit_button = buttons[1]
		self.cancel_button = buttons[2]

		inputs = self.cont.find_elements_by_tag_name('input')
		self.name_input = inputs[0]
		self.facility_input = inputs[2]
		self.city_input = inputs[3]

		self.state_cont = self.cont.find_element_by_class_name('stateFont')
		try:
			self.state_selector = self.state_cont.find_element_by_class_name('Select-placeholder')
		except NoSuchElementException:
			self.state_selector = self.state_cont.find_element_by_class_name('Select-value')

		# self.validate()
		return True

	# def validate(self):
	# 	pass

	def set_state(self, value):
		# Click value div if already set. Placeholder if not set
		self.state_selector.click()

		# Load dropdown options
		dropdownOptions = {}
		try:
			menu = self.state_cont.find_element_by_class_name('Select-menu-outer')
			divs = menu.find_elements_by_tag_name('div')
			for i, div in enumerate(divs):
				if i != 0: # First div is container
					dropdownOptions[div.text.lower()] = divs[i]
		except NoSuchElementException:
			print('AddPhysicianForm: Unable to find dropdown items for physician state')

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

	def submit(self, physicianInfo, action='submit'):
		if physicianInfo:
			if physicianInfo['name']:
				self.name_input.click()
				AC(self.driver).send_keys(physicianInfo['name']).perform()

			if physicianInfo['facility']:
				self.facility_input.clear()
				self.facility_input.send_keys(physicianInfo['facility'])
			if physicianInfo['city']:
				self.city_input.clear()
				self.city_input.send_keys(physicianInfo['city'])
			if physicianInfo['state']:
				self.set_state(physicianInfo['state'])

			if action == 'submit':
				self.submit_button.click()
			elif action == 'cancel':
				self.cancel_button.click()
			elif action == 'close':
				self.close_button.click()
			return True
		return False

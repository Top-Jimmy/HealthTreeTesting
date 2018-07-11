from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class UploadFileForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.container = self.driver.find_element_by_class_name('modal-content')
		buttons = self.container.find_elements_by_tag_name('button')

		self.close_button = buttons[0]

		upload_file_div = self.container.find_element_by_class_name('dropzone_div')

		self.continue_button = buttons[1]
		self.cancel_button = buttons[2]
		
		return self.validate()

	def validate(self):
		failures = []
		if self.continue_button.text != 'CONTINUE':
			failures.append('NewAccoutPopUpForm: Unexpected continue button text: "' + self.continue_button.text + '"')
		if self.cancel_button.text != 'CANCEL':
			failures.append('NewAccountPopUpForm: Unexpected cancel button text: "' + self.cancel_button.text + '"')
		if len(failures) > 0:
			for failure in failures:
				print(failure)
			return False
			# raise NoSuchElementException('Failed to load PopUpForm')
		return True

	def confirm(self, action='continue'):
		if action == 'continue':
			self.continue_button.click()
		else: 
			self.cancel_button.click()
		return True


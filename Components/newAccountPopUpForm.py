from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class NewAccountPopUpForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.container = self.driver.find_element_by_class_name('modal-content')
		buttons = self.container.find_elements_by_tag_name('button')

		self.yes_button = buttons[0]
		self.no_button = buttons[1]
		
		return self.validate()

	def validate(self):
		failures = []
		if self.yes_button.text != 'Yes':
			failures.append('NewAccoutPopUpForm: Unexpected yes button text: "' + self.yes_button.text + '"')
		if self.no_button.text != 'No':
			failures.append('NewAccountPopUpForm: Unexpected no button text: "' + self.no_button.text + '"')
		if len(failures) > 0:
			for failure in failures:
				print(failure)
			return False
			# raise NoSuchElementException('Failed to load PopUpForm')
		return True

	def confirm(self, action='yes'):
		if action == 'yes':
			self.yes_button.click()
		else:
			self.no_button.click()
		return True


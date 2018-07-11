from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class PopUpForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.container = self.driver.find_element_by_class_name('react-confirm-alert')
		buttons = self.container.find_elements_by_tag_name('button')

		self.confirm_button = buttons[0]
		if len(buttons) > 1:
			self.cancel_button = buttons[1]
		else:
			self.cancel_button = None
		return self.validate()

	def validate(self):
		failures = []
		if self.confirm_button.text != 'Confirm':
			failures.append('PopUpForm: Unexpected confirm button text: "' + self.confirm_button.text + '"')
		if self.cancel_button and self.cancel_button.text != 'Cancel':
			failures.append('PopUpForm: Unexpected cancel button text: "' + self.cancel_button.text + '"')
		if len(failures) > 0:
			for failure in failures:
				print(failure)
			return False
			# raise NoSuchElementException('Failed to load PopUpForm')
		return True

	def confirm(self, popUpAction='confirm'):
		if popUpAction == 'confirm':
			self.confirm_button.click()
		else:
			self.cancel_button.click()
		return True


from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class ConfirmPasswordForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		buttons = self.form.find_elements_by_tag_name('button')

		self.confirm_password_input = self.form.find_element_by_tag_name('input')

		self.continue_button = buttons[1]
		self.cancel_button = buttons[2]
		return self.validate()

	def validate(self):
		failures = []
		if self.continue_button.text.lower() != 'continue':
			failures.append('PopUpForm: Unexpected confirm button text: "' + self.continue_button.text + '"')
		if self.cancel_button.text.lower() != 'cancel':
			failures.append('PopUpForm: Unexpected cancel button text: "' + self.cancel_button.text + '"')
		if len(failures) > 0:
			for failure in failures:
				print(failure)
			return False
			# raise NoSuchElementException('Failed to load PopUpForm')
		return True

	def submit(self, formData, confirmAction='continue'):
		if formData:
			self.confirm_password_input.send_keys(formData['password'])

		if confirmAction == 'continue':
			self.continue_button.click()
		else:
			self.cancel_button.click()
		return True

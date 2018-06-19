from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class PopUpForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		form = self.driver.find_element_by_tag_name('form')
		inputs = self.form.find_element_by_tag_name('input')

		self.dateDiagnosis_cont = self.form.find_element_by_class_name('mnth-datepicker')
		self.dateDiagnosis_input = self.dateDiagnosis_cont.find_element_by_tag_name('input')

		self.gain_1q21_checkbox = inputs[]

		self.save_button = buttons[]
		self.cancel_button = buttons[]
		return self.validate()

	def validate(self):
		failures = []
		if self.confirm_button.text != 'Confirm':
			failures.append('PopUpForm: Unexpected confirm button text: ' + self.confirm_button.text)
		if self.cancel_button.text != 'Cancel':
			failures.append('PopUpForm: Unexpected cancel button text ' + self.cancel_button.text)
		if len(failures) > 0:
			for failure in failures:
				print(failure)
			return False
			# raise NoSuchElementException('Failed to load PopUpForm')
		return True

	def confirm(self, action='submit'):
		if action == 'submit':
			self.confirm_button.click()
		else:
			self.cancel_button.click()
		return True


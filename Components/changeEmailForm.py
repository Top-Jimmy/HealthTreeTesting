from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
import time

class ChangeEmailForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		buttons = self.form.find_elements_by_tag_name('button')
		inputs = self.form.find_elements_by_tag_name('input')

		self.close_button = buttons[0]
		self.new_email_input = inputs[1]

		self.continue_button = buttons[1]
		self.cancel_button = buttons[2]
		return True

	def submit(self, formData, action='cancel'):
		if formData['new_email']:
			self.new_email_input.send_keys(formData['new_email'])

		if action == 'continue':
			self.continue_button.click()
		else:
			self.cancel_button.click()
		return True


from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class ChangePasswordForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		buttons = self.form.find_elements_by_tag_name('button')
		inputs = self.form.find_elements_by_tag_name('input')

		self.close_button = buttons[0]

		self.current_password_input = inputs[0]

		self.new_password_input = inputs[1]
		self.confirm_password_input = inputs[2]

		self.continue_button = buttons[1]
		self.cancel_button = buttons[2]
		# return self.validate()
		return True

	def submit(self, passwordInfo, otherpasswordInfo, action='continue'):
		self.current_password_input.send_keys(passwordInfo['old_password'])
		self.new_password_input.send_keys(passwordInfo['new_password'])
		self.confirm_password_input.send_keys(passwordInfo['new_password'])

		if action == 'continue':
			self.continue_button.click()
		else:
			self.cancel_button.click()
		return True


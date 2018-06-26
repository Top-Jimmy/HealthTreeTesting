from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class ChangeUsernameForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		buttons = self.form.find_elements_by_tag_name('button')
		inputs = self.form.find_elements_by_tag_name('input')

		self.close_button = buttons[0]

		self.new_username_input = inputs[1]

		self.continue_button = buttons[1]
		self.cancel_button = buttons[2]
		# return self.validate()
		return True

	def submit(self, usernameInfo, otherusernameInfo, action='continue'):
		if usernameInfo['new_username']:
			self.new_username_input.send_keys(usernameInfo['new_username'])

		if action == 'continue':
			self.continue_button.click()
		else:
			self.cancel_button.click()
		return True


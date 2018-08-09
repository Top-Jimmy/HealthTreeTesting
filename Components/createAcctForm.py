import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class CreateAcctForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_element_by_tag_name('form')
		anchors = self.form.find_elements_by_tag_name('a')
		small = self.form.find_elements_by_tag_name('small')

		self.username_input = self.form.find_element_by_id('username_1')
		self.username_warning = small[0]

		self.email_input = self.form.find_element_by_id('email')
		self.email_warning = small[1]

		self.phone_input = self.form.find_element_by_id('user_phone_1')

		self.password_input = self.form.find_element_by_id('password')
		self.password_warning = small[5]

		self.confirm_password_input = self.form.find_element_by_id('confirm_password')
		self.confirm_password_warning = small[6]

		self.submit_button = self.form.find_element_by_tag_name('button')

		self.validate()

		return True


	def validate(self):
		failures = []
		inputs = self.form.find_elements_by_tag_name('input')
		if len(inputs) != 5:
			failures.append('Unexpected number of inputs: ' + str(len(inputs)))


		if len(failures) > 0:
			for failure in failures:
				print(failure)
			raise NoSuchElementException('Failed to load createAcctForm')


		return True

	def submit(self, acctInfo, action):
		warnings = []
		if acctInfo:
			self.username_input.clear()
			self.username_input.send_keys(acctInfo['username'])

			self.email_input.clear()
			self.email_input.send_keys(acctInfo['email'])

			self.phone_input.clear()
			self.phone_input.send_keys(acctInfo['phone'])

			self.password_input.clear()
			self.password_input.send_keys(acctInfo['password'])

			self.confirm_password_input.clear()
			self.confirm_password_input.send_keys(acctInfo['password'])

			if action == 'fail':
				self.submit_button.click()
			else:
				pass

			if len(self.username_warning.text) > 1:
				warnings.append(self.username_warning.text)
			if len(self.email_warning.text) > 1:
				warnings.append(self.email_warning.text)
			if len(self.password_warning.text) > 1:
				warnings.append(self.password_warning.text)
			if len(self.confirm_password_warning.text) > 1:
				warnings.append(self.confirm_password_warning.text)

			if action == 'fail' and len(warnings) != 0:
				for warning in warnings:
					print(warning)
				return True
			if action == 'fail' and len(warnings) == 0:
				print('Expected errors, none were detected')
				return False


			if len(warnings) > 0:
				for warning in warnings:
					print(warning)
				raise NoSuchElementException('Could not create account')

			return True
		return False







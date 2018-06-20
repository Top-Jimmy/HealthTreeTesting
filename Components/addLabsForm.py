from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
import datePicker
import time


class AddLabsForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[1]
		buttons = self.form.find_elements_by_tag_name('button')

		# self.close_button = buttons[5]
		cont = self.driver.find_elements_by_class_name('date-picker-icon-div')
		self.dobd_input = self.cont.find_elements_by_tag_name('input')

		

		self.save_button = buttons[1]
		self.cancel_button = buttons[0]

		return True
	
	def submit(self, riskInfo, action='save'):
		if riskInfo:
			if riskInfo['high_b2m'] == 'yes':
				self.high_b2m_yes_radio.click()
			elif riskInfo['high_b2m'] == 'no':
				self.high_b2m_no_radio.click()
			else:
				self.high_b2m_idk_radio.click()

			if riskInfo['high_ldh'] == 'yes':
				self.high_ldh_yes_radio.click()
			elif riskInfo['high_ldh'] == 'no':
				self.high_ldh_no_radio.click()
			else:
				self.high_ldh_idk_radio.click()

			if riskInfo['low_albumin'] == 'yes':
				self.low_albumin_yes_radio.click()
			elif riskInfo['low_albumin'] == 'no':
				self.low_albumin_no_radio.click()
			else:
				self.low_albumin_idk_radio.click()

			if action == 'save':
				self.save_button.click()
			if action == 'cancel':
				self.cancel_button.click()
			if action == 'close':
				self.close_button.click()
			return True
		return False




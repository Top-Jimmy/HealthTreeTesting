from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
import datePicker
import time
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class GepTestForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

		self.form = self.driver.find_element_by_class_name('modal-content')
		buttons = self.form.find_elements_by_tag_name('button')
		self.rows = self.form.find_elements_by_class_name('form-group')

		self.close_button = buttons[0]

		if not self.rows:
			return False
		datepicker = self.rows[0].find_element_by_class_name('Select--single')

		self.comment_textarea = self.form.find_element_by_tag_name('textarea')

		self.save_button = buttons[2]
		self.cancel_button = buttons[1]

		return True

	def submit(self, gepInfo, action='cancel'):
		if gepInfo:
			if gepInfo['test_gep_date'] is not None:
				picker = datePicker.DatePicker(self.driver, self.rows[0])
			# self.dateDiagnosis_input.click()
			# picker.set_date(formInfo['diagnosis_date'], self.dateDiagnosis_input)
				dateSet = False
				while not dateSet:
					try:
						# self.dateDiagnosis_input.click()

						picker.set_date(gepInfo['test_gep_date'])
						dateSet = True
					except (ElementNotVisibleException, StaleElementReferenceException) as e:
						print('Failed to set date. Page probably reloaded')
						time.sleep(.4)

			if gepInfo['gep_comment']:
				self.comment_textarea.clear()
				self.comment_textarea.send_keys(gepInfo['gep_comment'])

			if action == 'save':
				self.save_button.click()
			if action == 'cancel':
				self.cancel_button.click()
			if action == 'close':
				self.close_button.click()
			return True
		return False


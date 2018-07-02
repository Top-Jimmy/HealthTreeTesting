from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
import datePicker
import time


class GepTestForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[1]
		buttons = self.form.find_elements_by_tag_name('button')
		self.rows = self.form.find_elements_by_class_name('form-group')

		# self.close_button = buttons[5]

		self.dateDiagnosis_cont = self.form.find_element_by_class_name('mnth-datepicker')
		self.dateDiagnosis_input = self.dateDiagnosis_cont.find_element_by_tag_name('input')

		self.comment_textarea = self.form.find_element_by_tag_name('textarea')

		self.save_button = buttons[1]
		self.cancel_button = buttons[0]

		return True
		# return self.validate(expectedValues)

	def submit(self, gepInfo, action='cancel'):
		if gepInfo:
			if gepInfo['test_gep_date'] is not None:
				picker = datePicker.DatePicker(self.driver, self.rows[0])
			# self.dateDiagnosis_input.click()
			# picker.set_date(formInfo['diagnosis_date'], self.dateDiagnosis_input)
				dateSet = False
				while not dateSet:
					try:
						self.dateDiagnosis_input.click()

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


 	

				



	# def confirm(self, action='submit'):
	# 	if action == 'submit':
	# 		self.confirm_button.click()
	# 	else:
	# 		self.cancel_button.click()
	# 	return True


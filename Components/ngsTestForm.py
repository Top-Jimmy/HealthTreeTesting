from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
import datePicker
import time
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class NgsTestForm():

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

		self.comment_textarea = self.form.find_element_by_id('exampleText')

		self.mutate_nras_checkbox = self.form.find_element_by_id('Ngsvalue_NRAS')
		self.mutate_kras_checkbox = self.form.find_element_by_id('Ngsvalue_KRAS')
		self.mutate_braf_checkbox = self.form.find_element_by_id('Ngsvalue_BRAF')
		self.mutate_tp53_checkbox = self.form.find_element_by_id('Ngsvalue_TP53')
		self.mutate_fam46c_checkbox = self.form.find_element_by_id('Ngsvalue_FAM46C')
		self.mutate_dis3_checkbox = self.form.find_element_by_id('Ngsvalue_DIS3')
		self.mutate_traf3_checkbox = self.form.find_element_by_id('Ngsvalue_TRAF3')
		self.mutate_fgfr3_checkbox = self.form.find_element_by_id('Ngsvalue_NRASFGFR3')
		self.mutate_atm_checkbox = self.form.find_element_by_id('Ngsvalue_ATM')

		self.save_button = buttons[2]
		self.cancel_button = buttons[1]

		return True
		# return self.validate(expectedValues)

	def submit(self, ngsInfo, action='save'):
		if ngsInfo:
			if ngsInfo['test_ngs_date'] is not None:
				picker = datePicker.DatePicker(self.driver, self.rows[0])
			# self.dateDiagnosis_input.click()
			# picker.set_date(formInfo['diagnosis_date'], self.dateDiagnosis_input)
				dateSet = False
				while not dateSet:
					try:
						# self.dateDiagnosis_input.click()

						picker.set_date(ngsInfo['test_ngs_date'])
						dateSet = True
					except (ElementNotVisibleException, StaleElementReferenceException) as e:
						print('Failed to set date. Page probably reloaded')
						time.sleep(.4)

			if ngsInfo['ngs_comment']:
				self.comment_textarea.clear()
				self.comment_textarea.send_keys('ngs_comment')

			if ngsInfo['mutate_nras'] != self.mutate_nras_checkbox.is_selected():
				self.mutate_nras_checkbox.click()
			if ngsInfo['mutate_kras'] != self.mutate_kras_checkbox.is_selected():
				self.mutate_kras_checkbox.click()
			if ngsInfo['mutate_braf'] != self.mutate_braf_checkbox.is_selected():
				self.mutate_braf_checkbox.click()
			if ngsInfo['mutate_tp53'] != self.mutate_tp53_checkbox.is_selected():
				self.mutate_tp53_checkbox.click()
			if ngsInfo['mutate_fam46c'] != self.mutate_fam46c_checkbox.is_selected():
				self.mutate_fam46c_checkbox.click()
			if ngsInfo['mutate_dis3'] != self.mutate_dis3_checkbox.is_selected():
				self.mutate_dis3_checkbox.click()
			if ngsInfo['mutate_traf3'] != self.mutate_traf3_checkbox.is_selected():
				self.mutate_traf3_checkbox.click()
			if ngsInfo['mutate_fgfr3'] != self.mutate_fgfr3_checkbox.is_selected():
				self.mutate_fgfr3_checkbox.click()
			if ngsInfo['mutate_atm'] != self.mutate_atm_checkbox.is_selected():
				self.mutate_atm_checkbox.click()

			if action == 'save':
				self.save_button.click()
			if action == 'cancel':
				self.cancel_button.click()
			if action == 'close':
				self.close_button.click()
			return True
		return False


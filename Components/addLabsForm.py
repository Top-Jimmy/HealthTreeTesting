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
		inputs = self.form.find_elements_by_tag_name('input')
		footer = self.driver.find_elements_by_class_name('modal-footer')
		buttons = self.footer.find_elements_by_tag_name('button')
		# self.close_button = buttons[5]
		cont = self.driver.find_elements_by_class_name('date-picker-icon-div')
		self.dobd_input = self.cont.find_elements_by_tag_name('input')
		

		self.monoclonal_input = inputs[0]
		self.kappa_free_input = inputs[1]
		self.lambda_free_input = inputs[2]
		self.ratio_input = inputs[3]
		self.urine_input = inputs[4]
		self.blood_input = inputs[5]

		self.calcium_input = inputs[6]
		self.platelets_input = inputs[7]
		self.blood_cell_input = inputs[8]
		self.hemoglobin_input = inputs[9]
		self.lactate_input = inputs[10]
		self.immuno_g_input = inputs[11]
		self.immuno_a_input = inputs[12]
		self.immuno_m_input = inputs[13]
		self.albumin_input = inputs[14]

		self.save_button = buttons[0]
		self.cancel_button = buttons[1]

		return True
	
	def submit(self, labInfo, action='save'):
		if labInfo:
			self.dobd_input.clear()
			self.dobd_input.send_keys(labInfo['dobd'])

			self.monoclonal_input.clear()
			self.monoclonal_input.send_keys(labInfo['monoclonal'])

			self.kappa_free_input.clear()
			self.kappa_free_input.send_keys(labInfo['kappa'])

			self.lambda_free_input.clear()
			self.lambda_free_input.send_keys(labInfo['lambda'])

			self.ratio_input.clear()
			self.ratio_input.send_keys(labInfo['ratio'])

			self.urine_input.clear()
			self.urine_input.send_keys(labInfo['urine'])

			self.blood_input.clear()
			self.blood_input.send_keys(labInfo['blood'])

			self.calcium_input.clear()
			self.calcium_input.send_keys(labInfo['calcium'])

			self.platelets_input.clear()
			self.platelets_input.send_keys(labInfo['platelets'])

			self.blood_cell_input.clear()
			self.blood_cell_input.send_keys(labInfo['blood_cell'])

			self.hemoglobin_input.clear()
			self.hemoglobin_input.send_keys(labInfo['hemoglobin'])

			self.lactate_input.clear()
			self.lactate_input.send_keys(labInfo['lactate'])

			self.immuno_g_input.clear()
			self.immuno_g_input.send_keys(labInfo['immuno_g'])

			self.immuno_a_input.clear()
			self.immuno_a_input.send_keys(labInfo['immuna_a'])

			self.immuno_m_input.clear()
			self.immuno_m_input.send_keys(labInfo['immuno_m'])

			self.albumin_input.clear()
			self.albumin_input.send_keys(labInfo['albumin'])

			if action == 'save':
				self.save_button.click()
			if action == 'cancel':
				self.cancel_button.click()
			if action == 'close':
				self.close_button.click()
			return True
		return False




from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
import datePicker
import time
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class AddLabsForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

		cont = self.driver.find_element_by_class_name('myeloma-labs-row')
		self.get_my_labs_button = cont.find_element_by_tag_name('button')
		self.lab_date = self.driver.find_element_by_id('dateField')

		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		# Has 2 sets of 8 inputs (not counting date)
		if (len(inputs) != 16):
			print('AddLabsForm has more inputs than it expects: ' + str(len(inputs)))
		self.monoclonal_input = inputs[0]
		self.kappa_free_input = inputs[1]
		self.lambda_free_input = inputs[2]
		self.ratio_input = inputs[3]
		self.marrow_input = inputs[4]
		self.creatinine_input = inputs[5]
		self.platelets_input = inputs[6]
		self.absolute_neutrophils = inputs[7]

		self.calcium_input = inputs[8]
		self.blood_cell_input = inputs[9]
		self.hemoglobin_input = inputs[10]
		self.lactate_input = inputs[11]
		self.immuno_g_input = inputs[12]
		self.immuno_a_input = inputs[13]
		self.immuno_m_input = inputs[14]
		self.albumin_input = inputs[15]

		self.footer = self.driver.find_element_by_class_name('modal-footer')
		footer_buttons = self.footer.find_elements_by_tag_name('button')
		self.save_button = footer_buttons[0]
		self.cancel_button = footer_buttons[1]
		return True

	def submit(self, labInfo, action='save'):
		time.sleep(3)
		if labInfo:
			self.lab_date.clear()
			self.lab_date.send_keys(labInfo['lab_date'])

			# 1: Clinical Trials
			self.monoclonal_input.clear()
			self.monoclonal_input.send_keys(labInfo['monoclonal'])
			self.kappa_free_input.clear()
			self.kappa_free_input.send_keys(labInfo['kappa'])
			self.lambda_free_input.clear()
			self.lambda_free_input.send_keys(labInfo['lambda'])
			self.ratio_input.clear()
			self.ratio_input.send_keys(labInfo['ratio'])
			self.marrow_input.clear()
			self.marrow_input.send_keys(labInfo['bone_marrow'])

			self.creatinine_input.clear()
			self.creatinine_input.send_keys(labInfo['platelets'])
			self.platelets_input.clear()
			self.platelets_input.send_keys(labInfo['platelets'])
			self.absolute_neutrophils.clear()
			self.absolute_neutrophils.send_keys(labInfo['neutrophils'])

			# 2: Current state
			self.calcium_input.clear()
			self.calcium_input.send_keys(labInfo['calcium'])
			self.blood_cell_input.clear()
			self.blood_cell_input.send_keys(labInfo['blood_cell'])
			self.hemoglobin_input.clear()
			self.hemoglobin_input.send_keys(labInfo['hemoglobin'])
			self.lactate_input.clear()
			self.lactate_input.send_keys(labInfo['lactate'])
			self.immuno_g_input.clear()
			self.immuno_g_input.send_keys(labInfo['immuno_g'])
			self.immuno_a_input.clear()
			self.immuno_a_input.send_keys(labInfo['immuno_a'])
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


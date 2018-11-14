from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
import datePicker
import time
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class FishTestForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		
		self.form = self.driver.find_elements_by_tag_name('form')[1]
		buttons = self.form.find_elements_by_tag_name('button')
		self.rows = self.form.find_elements_by_class_name('form-group')


		# Make sure datepicker row has right stuff loaded
		if not self.rows:
			return False
		datepicker = self.rows[0].find_element_by_class_name('Select--single')

		self.comment_textarea = self.rows[0].find_element_by_class_name('textarea')
		raw_input('comment area working')

		self.add_1q21_checkbox = self.form.find_element_by_id('fishtesting_Addition_1q21')
		raw_input('gene additions working')

		self.deletion_1p_checkbox = self.form.find_element_by_id('fishtesting_Deletion_1p')
		self.deletion_17p_checkbox = self.form.find_element_by_id('fishtesting_Deletion_17p')
		self.deletion_13q_checkbox = self.form.find_element_by_id('fishtesting_Deletion_13q')
		self.deletion_16q_checkbox = self.form.find_element_by_id('fishtesting_Deletion_16q')
		raw_input('gene deletions working')

		self.trans_FGFR3_checkbox =  self.form.find_element_by_id('fishtesting_Translocation_FGFR3')
		self.trans_CCND3_checkbox = self.form.find_element_by_id('fishtesting_Translocation_CCND3')
		self.trans_CCND1_checkbox = self.form.find_element_by_id('fishtesting_Translocation_CCND1')
		self.trans_cMAF_checkbox = self.form.find_element_by_id('fishtesting_Translocation_c-MAF')
		self.trans_MAFB_checkbox = self.form.find_element_by_id('fishtesting_Translocation_MAFB')
		self.trans_ETV6_checkbox = self.form.find_element_by_id('fishtesting_Translocation_ETV6')
		raw_input('gene translations working')

		self.tri_3_checkbox = self.form.find_element_by_id('fishtesting_Trisomies_3')
		self.tri_5_checkbox = self.form.find_element_by_id('fishtesting_Trisomies_5')
		self.tri_7_checkbox = self.form.find_element_by_id('fishtesting_Trisomies_7')
		self.tri_9_checkbox = self.form.find_element_by_id('fishtesting_Trisomies_9')
		self.tri_11_checkbox = self.form.find_element_by_id('fishtesting_Trisomies_11')
		self.tri_15_checkbox = self.form.find_element_by_id('fishtesting_Trisomies_15')
		self.tri_17_checkbox = self.form.find_element_by_id('fishtesting_Trisomies_17')
		self.tri_19_checkbox = self.form.find_element_by_id('fishtesting_Trisomies_19')

		self.tetra_3_checkbox = self.form.find_element_by_id('fishtesting_Tetrasomies_3')
		self.tetra_5_checkbox = self.form.find_element_by_id('fishtesting_Tetrasomies_5')
		self.tetra_7_checkbox = self.form.find_element_by_id('fishtesting_Tetrasomies_7')
		self.tetra_9_checkbox = self.form.find_element_by_id('fishtesting_Tetrasomies_9')
		self.tetra_11_checkbox = self.form.find_element_by_id('fishtesting_Tetrasomies_11')
		self.tetra_15_checkbox = self.form.find_element_by_id('fishtesting_Tetrasomies_15')
		self.tetra_17_checkbox = self.form.find_element_by_id('fishtesting_Tetrasomies_17')
		self.tetra_19_checkbox = self.form.find_element_by_id('fishtesting_Tetrasomies_19')

		self.save_button = buttons[1]
		self.cancel_button = buttons[0]

		return True

	def submit(self, fishInfo, action='save'):
		if fishInfo:
			if fishInfo['test_fish_date'] is not None:
				picker = datePicker.DatePicker(self.driver, self.rows[0])
			# self.dateDiagnosis_input.click()
			# picker.set_date(formInfo['diagnosis_date'], self.dateDiagnosis_input)
				dateSet = False
				while not dateSet:
					try:
						# self.dateDiagnosis_input.click()

						picker.set_date(fishInfo['test_fish_date'])
						dateSet = True
					except (ElementNotVisibleException, StaleElementReferenceException) as e:
						print('Failed to set date. Page probably reloaded')
						time.sleep(.4)

			if fishInfo['gene_additions']['1q21'] != self.add_1q21_checkbox.is_selected():
				self.add_1q21_checkbox.click()

			if fishInfo['gene_deletions']['deletion_1p'] != self.deletion_1p_checkbox.is_selected():
				self.deletion_1p_checkbox.click()
			if fishInfo['gene_deletions']['deletion_17p'] != self.deletion_17p_checkbox.is_selected():
				self.deletion_17p_checkbox.click()
			if fishInfo['gene_deletions']['deletion_13q'] != self.deletion_13q_checkbox.is_selected():
				self.deletion_13q_checkbox.click()
			if fishInfo['gene_deletions']['deletion_16q'] != self.deletion_16q_checkbox.is_selected():
				self.deletion_16q_checkbox.click()

			if fishInfo['gene_translocations']['trans_FGFR3'] != self.trans_FGFR3_checkbox.is_selected():
				self.trans_FGFR3_checkbox.click()
			if fishInfo['gene_translocations']['trans_CCND3'] != self.trans_CCND3_checkbox.is_selected():
				self.trans_CCND3_checkbox.click()
			if fishInfo['gene_translocations']['trans_CCND1'] != self.trans_CCND1_checkbox.is_selected():
				self.trans_CCND1_checkbox.click()
			if fishInfo['gene_translocations']['trans_cMAF'] != self.trans_cMAF_checkbox.is_selected():
				self.trans_cMAF_checkbox.click()
			if fishInfo['gene_translocations']['trans_MAFB'] != self.trans_MAFB_checkbox.is_selected():
				self.trans_MAFB_checkbox.click()
			if fishInfo['gene_translocations']['trans_ETV6'] != self.trans_ETV6_checkbox.is_selected():
				self.trans_ETV6_checkbox.click()

			if fishInfo['trisomies']['tri_3'] != self.tri_3_checkbox.is_selected():
				self.tri_3_checkbox.click()
			if fishInfo['trisomies']['tri_5'] != self.tri_5_checkbox.is_selected():
				self.tri_5_checkbox.click()
			if fishInfo['trisomies']['tri_7'] != self.tri_7_checkbox.is_selected():
				self.tri_7_checkbox.click()
			if fishInfo['trisomies']['tri_9'] != self.tri_9_checkbox.is_selected():
				self.tri_9_checkbox.click()
			if fishInfo['trisomies']['tri_11'] != self.tri_11_checkbox.is_selected():
				self.tri_11_checkbox.click()
			if fishInfo['trisomies']['tri_15'] != self.tri_15_checkbox.is_selected():
				self.tri_15_checkbox.click()
			if fishInfo['trisomies']['tri_17'] != self.tri_17_checkbox.is_selected():
				self.tri_17_checkbox.click()
			if fishInfo['trisomies']['tri_17'] != self.tri_17_checkbox.is_selected():
				self.tri_17_checkbox.click()

			if fishInfo['tetrasomies']['tetra_3'] != self.tetra_3_checkbox.is_selected():
				self.tetra_3_checkbox.click()
			if fishInfo['tetrasomies']['tetra_5'] != self.tetra_5_checkbox.is_selected():
				self.tetra_5_checkbox.click()
			if fishInfo['tetrasomies']['tetra_7'] != self.tetra_7_checkbox.is_selected():
				self.tetra_7_checkbox.click()
			if fishInfo['tetrasomies']['tetra_9'] != self.tetra_9_checkbox.is_selected():
				self.tetra_9_checkbox.click()
			if fishInfo['tetrasomies']['tetra_11'] != self.tetra_11_checkbox.is_selected():
				self.tetra_11_checkbox.click()
			if fishInfo['tetrasomies']['tetra_15'] != self.tetra_15_checkbox.is_selected():
				self.tetra_15_checkbox.click()
			if fishInfo['tetrasomies']['tetra_17'] != self.tetra_17_checkbox.is_selected():
				self.tetra_17_checkbox.click()
			if fishInfo['tetrasomies']['tetra_17'] != self.tetra_17_checkbox.is_selected():
				self.tetra_17_checkbox.click()

			if action == 'save':
				self.save_button.click()
			if action == 'cancel':
				self.cancel_button.click()
			if action == 'close':
				self.close_button.click()
			return True
		return False


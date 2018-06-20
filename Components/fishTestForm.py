from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
import datePicker
import time


class FishTestForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[1]
		buttons = self.form.find_elements_by_tag_name('button')

		# self.close_button = buttons[5]

		self.dateDiagnosis_cont = self.form.find_element_by_class_name('mnth-datepicker')
		self.dateDiagnosis_input = self.dateDiagnosis_cont.find_element_by_tag_name('input')

		self.three_1q21_checkbox = self.form.find_element_by_id('Addition_1q21_3copies')
		self.four_1q21_checkbox = self.form.find_element_by_id('Addition_1q21_4copies')

		self.deletion_1p_checkbox = self.form.find_element_by_id('Deletion_1p')
		self.deletion_17p_checkbox = self.form.find_element_by_id('Deletion_17p')
		self.deletion_13q_checkbox = self.form.find_element_by_id('Deletion_13q')
		self.deletion_16q_checkbox = self.form.find_element_by_id('Deletion_16q')

		self.trans_FGFR3_checkbox =  self.form.find_element_by_id('Translocation_FGFR3')
		self.trans_CCND3_checkbox = self.form.find_element_by_id('Translocation_CCND3')
		self.trans_CCND1_checkbox = self.form.find_element_by_id('Translocation_CCND1')
		self.trans_cMAF_checkbox = self.form.find_element_by_id('Translocation_c-MAF')
		self.trans_MAFB_checkbox = self.form.find_element_by_id('Translocation_MAFB')
		self.trans_ETV6_checkbox = self.form.find_element_by_id('Translocation_ETV6')

		self.tri_3_checkbox = self.form.find_element_by_id('Trisomies_3')
		self.tri_5_checkbox = self.form.find_element_by_id('Trisomies_5')
		self.tri_7_checkbox = self.form.find_element_by_id('Trisomies_7')
		self.tri_9_checkbox = self.form.find_element_by_id('Trisomies_9')
		self.tri_11_checkbox = self.form.find_element_by_id('Trisomies_11')
		self.tri_15_checkbox = self.form.find_element_by_id('Trisomies_15')
		self.tri_17_checkbox = self.form.find_element_by_id('Trisomies_17')
		self.tri_19_checkbox = self.form.find_element_by_id('Trisomies_19')

		self.tetra_3_checkbox = self.form.find_element_by_id('Tetrasomies_3')
		self.tetra_5_checkbox = self.form.find_element_by_id('Tetrasomies_5')
		self.tetra_7_checkbox = self.form.find_element_by_id('Tetrasomies_7')
		self.tetra_9_checkbox = self.form.find_element_by_id('Tetrasomies_9')
		self.tetra_11_checkbox = self.form.find_element_by_id('Tetrasomies_11')
		self.tetra_15_checkbox = self.form.find_element_by_id('Tetrasomies_15')
		self.tetra_17_checkbox = self.form.find_element_by_id('Tetrasomies_17')
		self.tetra_19_checkbox = self.form.find_element_by_id('Tetrasomies_19')

		self.save_button = buttons[1]
		self.cancel_button = buttons[0]

		return True
		# return self.validate(expectedValues)

	# def validate(self, expectedValues):
	# 	failures = []
	# 	if self.dateDiagnosis_input.get_attribute('value') != expectedValues['test_fish_date']:
	# 		failures.append('FishTestForm: Expecting date of diagnosis "' + expectedValues['date'] + '", got "' + self.dateDiagnosis_form-control.get_attribute('value') + '"')

	# 	if expectedValues['three_1q21'] != self.three_1q21_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['three_1q21']) + '" gene additions')
	# 	if expectedValues['four_1q21'] != self.four_1q21_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['four_1q21']) + '" gene additions')

	# 	if expectedValues['deletion_1p'] != self.deletion_1p_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['deletion_1p']) + '" gene deletion')
	# 	if expectedValues['deletion_17p'] != self.deletion_17p_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['deletion_17p']) + '" gene deletion')
	# 	if expectedValues['deletion_13q'] != self.deletion_13q_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['deletion_13q']) + '" gene deletion')
	# 	if expectedValues['deletion_16q'] != self.deletion_16q_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['deletion_16q']) + '" gene deletion')

	# 	if expectedValues['trans_FGFR3'] != self.trans_FGFR3_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['trans_FGFR3']) + '" gene translocation')
	# 	if expectedValues['trans_CCND3'] != self.trans_CCND3_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['trans_CCND3']) + '" gene translocation')
	# 	if expectedValues['trans_CCND1'] != self.trans_CCND1_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['trans_CCND1']) + '" gene translocation')
	# 	if expectedValues['trans_cMAF'] != self.trans_cMAF_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['trans_cMAF']) + '" gene translocation')
	# 	if expectedValues['trans_MAFB'] != self.trans_MAFB_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['trans_MAFB']) + '" gene translocation')
	# 	if expectedValues['trans_ETV6'] != self.trans_ETV6_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['trans_ETV6']) + '" gene translocation')

	# 	if expectedValues['tri_3'] != self.tri_3_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tri_3']) + '" trisomy')
	# 	if expectedValues['tri_5'] != self.tri_5_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tri_5']) + '" trisomy')
	# 	if expectedValues['tri_7'] != self.tri_7_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tri_7']) + '" trisomy')
	# 	if expectedValues['tri_9'] != self.tri_9_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tri_9']) + '" trisomy')
	# 	if expectedValues['tri_11'] != self.tri_11_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tri_11']) + '" trisomy')
	# 	if expectedValues['tri_15'] != self.tri_15_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tri_15']) + '" trisomy')
	# 	if expectedValues['tri_17'] != self.tri_17_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tri_17']) + '" trisomy')
	# 	if expectedValues['tri_19'] != self.tri_19_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tri_19']) + '" trisomy')

	# 	if expectedValues['tetra_3'] != self.tetra_3_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tetra_3']) + '" tetrasomy')
	# 	if expectedValues['tetra_5'] != self.tetra_5_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tetra_5']) + '" tetrasomy')
	# 	if expectedValues['tetra_7'] != self.tetra_7_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tetra_7']) + '" tetrasomy')
	# 	if expectedValues['tetra_9'] != self.tetra_9_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tetra_9']) + '" tetrasomy')
	# 	if expectedValues['tetra_11'] != self.tetra_11_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tetra_11']) + '" tetrasomy')
	# 	if expectedValues['tetra_15'] != self.tetra_15_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tetra_15']) + '" tetrasomy')
	# 	if expectedValues['tetra_17'] != self.tetra_17_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tetra_17']) + '" tetrasomy')
	# 	if expectedValues['tetra_19'] != self.tetra_19_checkbox.get_attribute('checked'):
	# 		failure.append('FishTestForm: Expected "' + str(expectedValues['tetra_19']) + '" tetrasomy')

	# 	if self.save_button.text != 'Save':
	# 		failures.append('PopUpForm: Unexpected save button text: ' + self.save_button.text)
	# 	if self.cancel_button.text != 'Cancel':
	# 		failures.append('PopUpForm: Unexpected cancel button text ' + self.cancel_button.text)

	# 	if len(failures) > 0:
	# 		for failure in failures:
	# 			print(failure)
	# 		return False
	# 		# raise NoSuchElementException('Failed to load PopUpForm')
	# 	return True

	def submit(self, fishInfo, action='save'):
		if fishInfo:
			if fishInfo['test_fish_date'] is not None:
				picker = datePicker.DatePicker(self.driver)
			# self.dateDiagnosis_input.click()
			# picker.set_date(formInfo['diagnosis_date'], self.dateDiagnosis_input)
				dateSet = False
				while not dateSet:
					try:
						self.dateDiagnosis_input.click()

						picker.set_date(fishInfo['test_fish_date'])
						dateSet = True
					except (ElementNotVisibleException, StaleElementReferenceException) as e:
						print('Failed to set date. Page probably reloaded')
						time.sleep(.4)

			if fishInfo['three_1q21'] != self.three_1q21_checkbox.is_selected():
				self.three_1q21_checkbox.click()
			if fishInfo['four_1q21'] != self.four_1q21_checkbox.is_selected():
				self.four_1q21_checkbox.click()

			if fishInfo['deletion_1p'] != self.deletion_1p_checkbox.is_selected():
				self.deletion_1p_checkbox.click()
			if fishInfo['deletion_17p'] != self.deletion_17p_checkbox.is_selected():
				self.deletion_17p_checkbox.click()
			if fishInfo['deletion_13q'] != self.deletion_13q_checkbox.is_selected():
				self.deletion_13q_checkbox.click()
			if fishInfo['deletion_16q'] != self.deletion_16q_checkbox.is_selected():
				self.deletion_16q_checkbox.click()

			if fishInfo['trans_FGFR3'] != self.trans_FGFR3_checkbox.is_selected():
				self.trans_FGFR3_checkbox.click()
			if fishInfo['trans_CCND3'] != self.trans_CCND3_checkbox.is_selected():
				self.trans_CCND3_checkbox.click()
			if fishInfo['trans_CCND1'] != self.trans_CCND1_checkbox.is_selected():
				self.trans_CCND1_checkbox.click()
			if fishInfo['trans_cMAF'] != self.trans_cMAF_checkbox.is_selected():
				self.trans_cMAF_checkbox.click()
			if fishInfo['trans_MAFB'] != self.trans_MAFB_checkbox.is_selected():
				self.trans_MAFB_checkbox.click()
			if fishInfo['trans_ETV6'] != self.trans_ETV6_checkbox.is_selected():
				self.trans_ETV6_checkbox.click()

			if fishInfo['tri_3'] != self.tri_3_checkbox.is_selected():
				self.tri_3_checkbox.click()
			if fishInfo['tri_5'] != self.tri_5_checkbox.is_selected():
				self.tri_5_checkbox.click()
			if fishInfo['tri_7'] != self.tri_7_checkbox.is_selected():
				self.tri_7_checkbox.click()
			if fishInfo['tri_9'] != self.tri_9_checkbox.is_selected():
				self.tri_9_checkbox.click()
			if fishInfo['tri_11'] != self.tri_11_checkbox.is_selected():
				self.tri_11_checkbox.click()
			if fishInfo['tri_15'] != self.tri_15_checkbox.is_selected():
				self.tri_15_checkbox.click()
			if fishInfo['tri_17'] != self.tri_17_checkbox.is_selected():
				self.tri_17_checkbox.click()
			if fishInfo['tri_17'] != self.tri_17_checkbox.is_selected():
				self.tri_17_checkbox.click()

			if fishInfo['tetra_3'] != self.tetra_3_checkbox.is_selected():
				self.tetra_3_checkbox.click()
			if fishInfo['tetra_5'] != self.tetra_5_checkbox.is_selected():
				self.tetra_5_checkbox.click()
			if fishInfo['tetra_7'] != self.tetra_7_checkbox.is_selected():
				self.tetra_7_checkbox.click()
			if fishInfo['tetra_9'] != self.tetra_9_checkbox.is_selected():
				self.tetra_9_checkbox.click()
			if fishInfo['tetra_11'] != self.tetra_11_checkbox.is_selected():
				self.tetra_11_checkbox.click()
			if fishInfo['tetra_15'] != self.tetra_15_checkbox.is_selected():
				self.tetra_15_checkbox.click()
			if fishInfo['tetra_17'] != self.tetra_17_checkbox.is_selected():
				self.tetra_17_checkbox.click()
			if fishInfo['tetra_17'] != self.tetra_17_checkbox.is_selected():
				self.tetra_17_checkbox.click()

			if action == 'save':
				self.save_button.click()
			if action == 'cancel':
				self.cancel_button.click()
			if action == 'close':
				self.close_button.click()
			return True
		return False



# ############ Saved Form ############
#  def edit_fish_test(self)

 	

				



	# def confirm(self, action='submit'):
	# 	if action == 'submit':
	# 		self.confirm_button.click()
	# 	else:
	# 		self.cancel_button.click()
	# 	return True


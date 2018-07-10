from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class ImagingSurveyForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		form = self.driver.find_elements_by_tag_name('form')[-2]
		buttons = form.find_elements_by_tag_name('button')
		inputs = form.find_elements_by_tag_name('input')

		self.xray_input = inputs[0]
		self.wbldct_input = inputs[1]
		self.spinal_input = inputs[2]
		self.whole_mri_input = inputs[3]
		self.bonescan_input = inputs[4]
		self.petct_input = inputs[5]
		self.petmri_input = inputs[6]
		self.bone_density_input = inputs[7]

		self.since_xray_input = inputs[8]
		self.since_wbldct_input = inputs[9]
		self.since_spinal_input = inputs[10]
		self.since_whole_mri_input = inputs[11]
		self.since_bonescan_input = inputs[12]
		self.since_petct_input = inputs[13]
		self.since_petmri_input = inputs[14]
		self.since_bone_density_input = inputs[15]

		self.save_button = buttons[1]
		self.cancel_button = buttons[2]
		# return self.validate()
		return True

	def submit(self, imagingInfo, action='cancel'):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		time.sleep(.5)
		if imagingInfo['xray'] != self.xray_input.is_selected():
			self.xray_input.click()
			
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['wbldct'] != self.wbldct_input.is_selected():
			self.wbldct_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['spinal'] != self.since_spinal_input.is_selected():
			self.since_spinal_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['whole_mri'] != self.whole_mri_input.is_selected():
			self.whole_mri_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['bonescan'] != self.bonescan_input.is_selected():
			self.bonescan_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['petct'] != self.petct_input.is_selected():
			self.petct_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['petmri'] != self.petmri_input.is_selected():
			self.petmri_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['bone_density'] != self.bone_density_input.is_selected():
			self.bone_density_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['since_xray'] != self.since_xray_input.is_selected():
			self.since_xray_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['since_wbldct'] != self.since_wbldct_input.is_selected():
			self.since_wbldct_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['since_spinal'] != self.since_spinal_input.is_selected():
			self.since_spinal_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['since_whole_mri'] != self.since_whole_mri_input.is_selected():
			self.since_whole_mri_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['since_bonescan'] != self.since_bonescan_input.is_selected():
			self.since_bonescan_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['since_petct'] != self.since_petct_input.is_selected():
			self.since_petct_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['since_petmri'] != self.since_petmri_input.is_selected():
			self.since_petmri_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if imagingInfo['since_bone_density'] != self.since_bone_density_input.is_selected():
			self.since_bone_density_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

		raw_input('is info there?')

		if action == 'save':
			self.save_button.click()
		else:
			self.cancel_button.click()
		return True


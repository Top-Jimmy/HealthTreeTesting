from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class MultipleMyelomaSurveyForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		form = self.driver.find_elements_by_tag_name('form')[-2]
		buttons = form.find_elements_by_tag_name('button')
		inputs = self.driver.find_elements_by_class_name('dynamic-radio')

		self.fish_checkbox = inputs[0]
		self.cytogenetics_checkbox = inputs[1]
		self.gep_checkbox = inputs[2]
		self.ngs_checkbox = inputs[3]
		self.idk_checkbox = inputs[4]
		self.none_checkbox = inputs[5]

		self.since_fish_checkbox = inputs[6]
		self.since_cytogenetics_checkbox = inputs[7]
		self.since_gep_checkbox = inputs[8]
		self.since_ngs_checkbox = inputs[9]
		self.since_idk_checkbox = inputs[10]
		self.since_none_checkbox = inputs[11]

		self.comment_textarea = form.find_element_by_tag_name('textarea')

		self.save_button = buttons[1]
		self.cancel_button = buttons[2]
		# return self.validate()
		return True
		

	def submit(self, myelomaInfo, action='cancel'):
		
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if myelomaInfo['fish'] != self.fish_checkbox.is_selected():
			time.sleep(.5)
			self.fish_checkbox.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))	
		if myelomaInfo['cytogenetics'] != self.cytogenetics_checkbox.is_selected():
			self.cytogenetics_checkbox.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if myelomaInfo['gep'] != self.gep_checkbox.is_selected():
			self.gep_checkbox.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if myelomaInfo['ngs'] != self.ngs_checkbox.is_selected():
			self.ngs_checkbox.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if myelomaInfo['idk'] != self.idk_checkbox.is_selected():
			self.idk_checkbox.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if myelomaInfo['none'] != self.none_checkbox.is_selected():
			self.none_checkbox.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if myelomaInfo['since_fish'] != self.since_fish_checkbox.is_selected():
			self.since_fish_checkbox.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if myelomaInfo['since_cytogenetics'] != self.since_cytogenetics_checkbox.is_selected():
			self.since_cytogenetics_checkbox.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if myelomaInfo['since_gep'] != self.since_gep_checkbox.is_selected():
			self.since_gep_checkbox.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if myelomaInfo['since_ngs'] != self.since_ngs_checkbox.is_selected():
			self.since_ngs_checkbox.click()

			WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			if myelomaInfo['since_idk'] != self.since_idk_checkbox.is_selected():
				self.since_idk_checkbox.click()

			WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			if myelomaInfo['since_none'] != self.since_none_checkbox.is_selected():
				self.since_none_checkbox.click()

			WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			if myelomaInfo['comment']:
				self.comment_textarea.send_keys(myelomaInfo['comment'])
			raw_input('correct info?')


			WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			if action == 'save':
				self.save_button.click()
			else:
				self.cancel_button.click()
			return True
		


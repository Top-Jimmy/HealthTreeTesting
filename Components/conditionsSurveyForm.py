from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class ConditionsSurveyForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		time.sleep(.5)
		form = self.driver.find_elements_by_tag_name('form')[-2]
		buttons = form.find_elements_by_tag_name('button')
		inputs = form.find_elements_by_tag_name('input')

		self.study_yes_input = inputs[0]
		self.study_no_input = inputs[1]

		self.save_button = buttons[1]
		self.cancel_button = buttons[2]
		# return self.validate()
		return True

	def submit(self, conditionsInfo, action='cancel'):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if conditionsInfo['participate'] == 'yes':
			self.study_yes_input.click()
		else:
			self.study_no_input.click()

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		if action == 'save':
			self.save_button.click()
		else:
			self.cancel_button.click()
		return True


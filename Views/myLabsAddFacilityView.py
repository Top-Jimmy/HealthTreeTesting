from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from Components import popUpForm
from Components import menu
from Components import header
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MyLabsAddFacilityView(view.View):
	post_url = 'add-facility'

	def load(self, expectedInfo=None):
		try:
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)

			self.container = self.driver.find_element_by_id('page-content-wrapper')
			self.facility_input = self.driver.find_element_by_id('facility_name')

			# Buttons not in order displayed (float right)
			buttons = self.container.find_elements_by_class_name('green-hvr-bounce-to-top')
			self.continue_button = buttons[0]
			self.back_button = buttons[1]

			return self.validate(expectedInfo)
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def validate(self, expectedInfo):
		failures = []
		# if self.add_facility_button.text != 'Click to add a facility':
		# 	failure.append('GetMyLabsView: Unexpected add facility button text')

		if expectedInfo:
			# Validate facilities
			pass

		if len(failures) > 0:
			for failure in failures:
				print(failure)
				return False
		return True

	def set_facility(self, facilityName):
		self.facility_input.clear()
		self.facility_input.send_keys(facilityName)
		self.continue_button.click()




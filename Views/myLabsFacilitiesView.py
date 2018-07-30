from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from Components import popUpForm
from Components import menu
from Components import header
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MyLabsFacilitiesView(view.View):
	post_url = 'my-labs-facilities'

	def load(self, expectedInfo=None):
		try:
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)

			self.container = self.driver.find_element_by_id('page-content-wrapper')
			self.add_facility_button = self.container.find_element_by_class_name('addDiagnoisisButton')

			# Not in order displayed (float right)
			self.action_buttons = self.container.find_elements_by_class_name('green-hvr-bounce-to-top')
			self.facilities = self.load_facilities()

			return self.validate(expectedInfo)
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def validate(self, expectedInfo):
		failures = []
		if self.add_facility_button.text != 'Click to add a facility':
			failure.append('GetMyLabsView: Unexpected add facility button text')

		if expectedInfo:
			# Validate facilities
			pass

		if len(failures) > 0:
			for failure in failures:
				print(failure)
			return False
		return True

	def num_facilities(self):
		if self.facilities:
			return len(self.facilities)
		return 0

	def load_facilities(self):
		facilities = []
		try:
			self.table = self.driver.find_element_by_id('facilities_table')
		except NoSuchElementException:
			self.table = None

		if self.table:
			rows = self.table.find_elements_by_tag_name('tr')
			for rowIndex, row in enumerate(rows):
				if rowIndex != 0: # Ignore table header
					facility = {}
					tds = row.find_elements_by_tag_name('td')
					for tdIndex, td in enumerate(tds):
						if tdIndex == 0:
							facility['name'] = td.text
						elif tdIndex == 1:
							buttons = td.find_elements_by_tag_name('button')
							facility['edit'] = buttons[0]
							facility['delete'] = buttons[1]
					facilities.append(facility)
		return facilities

################################# Test Functions #################################

	def manage_facility(self, facilityIndex, action):
		if action != 'delete' and action != 'edit':
			print('Invalid facility action: ' + str(action))
			return False

		facility = None
		try:
			facility = self.facilities[facilityIndex]
		except IndexError:
			print('Invalid facility index')
			return False

		if facility:
			facility[action].click()

			if action == 'delete':
				self.popUpForm = popUpForm.PopUpForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
				self.popUpForm.confirm('confirm')
				# Wait for confirm popup and loading overlay to disappear
				WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'react-confirm-alert')))
				WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			return True

	def delete_all(self):
		for i, facility in enumerate(self.facilities):
			self.manage_facility(i, 'delete')



import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class Menu():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		cont = self.driver.find_element_by_id('sidebar-wrapper')
		self.form = cont.find_element_by_tag_name('form')
		self.list_items = self.form.find_elements_by_tag_name('li')
		self.menu_options = {}

		# Loading full menu or basic menu for new user?
		self.menu_type = self.calculate_menu_type()
		if self.menu_type == 'normal':
			for i, option in enumerate(self.list_items):
				self.menu_options[option.text] = self.list_items[i]
			# self.about_me = self.li[0]
			# self.myeloma_diagnosis = self.li[1]
			# self.current_health = self.li[2]
			# self.fitness_level = self.li[3]
			# self.myeloma_genetics = self.li[4]
			# self.treatments_outcomes = self.li[5]
			# self.treatment_options = self.li[6]
			# self.clinical_trials = self.li[7]
			# self.myeloma_labs = self.li[8]
			# self.health_profile = self.li[9]
			# self.summary = self.li[10]
			# self.reports = self.li[11]
			# self.surveys = self.li[12]
			# self.settings = self.li[13]

		# self.validate()
		return True

	def calculate_menu_type(self):
		menuType = 'new'
		print(len(self.list_items))
		if len(self.list_items) > 10:
			menuType = 'normal'
		return menuType

	# Not sure if we need to validate anything. Text should match by nature of how we're loading LIs
	# def validate(self):
	# 	failures = []
	# 	if self.menu_options[i].text != 'About Me':
	# 		failures.append('1. About Me. Expecting text "About Me", got "' + self.about_me.text + '"')
	# 	if self.myeloma_diagnosis.text != 'About Me':
	# 		failures.append('2. Myeloma Diagnosis. Expecting text "Myeloma Diagnosis", got "' + self.myeloma_diagnosis.text + '"')
	# 	if len(failures) > 0:
	# 		print(failures)
	# 		raise NoSuchElementException('Failed to load CreateAcctForm')

	def go_to(self, destination):
		"""Go to given page in menu. Destination should match text in menu."""
		option = self.menu_options[destination]
		if option:
			self.driver.execute_script('arguments[0].scrollIntoView();', option)
			option.click()
		else:
			print('Menu: Unexpected destination: ' + destination)
			return False




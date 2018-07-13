from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError
from Components import fullHealthMyelomaForm, healthDemoForm, healthHistForm, famHistForm, healthLifestyleForm, healthQualityForm
from Components import menu
from Components import header
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class FullHealthView(view.View):

	def load(self, expectedTab=None):
		try:
			# Crap on left
			self.menu_tabs = self.driver.find_element_by_class_name('RRT__tabs')
			self.fullHealthMyelomaForm = fullHealthMyelomaForm.FullHealthMyelomaForm(self.driver)
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)

			self.load_tabs()
			self.selectedTab = self.selected_tab()
			if expectedTab and expectedTab != self.selectedTab:
				print('Full Health Profile: Expected state: "' + expectedTab + '", got state: "' + self.selectedTab + '"')
			else: 
				if expectedTab == 'my myeloma':
					self.fullHealthMyelomaForm = fullHealthMyelomaForm.FullHealthMyelomaForm(self.driver)
				elif expectedTab == 'demographics':
					self.healthDemoForm = healthDemoForm.HealthDemoForm(self.driver)
				elif expectedTab == 'full health history':
					self.healthHistForm = healthHistForm.HealthHistForm(self.driver)
				elif expectedTab == 'family history':
					self.famHistForm = famHistForm.FamHistForm(self.driver)
				elif expectedTab == 'lifestyle':
					self.healthLifestyleForm = healthLifestyleForm.HealthLifestyleForm(self.driver)
				elif expectedTab == 'quality of life':
					self.healthQualityForm = healthQualityForm.HealthQualityForm(self.driver)
				else:
					self.healthSummaryForm = healthSummaryForm.HealthSummaryForm(self.driver)


			self.myeloma_tab = self.menu_tabs.find_element_by_id('tab-0')
			self.demographics_tab = self.menu_tabs.find_element_by_id('tab-1')
			self.health_history_tab = self.menu_tabs.find_element_by_id('tab-2')
			self.family_history_tab = self.menu_tabs.find_element_by_id('tab-3')
			self.lifestyle_tab = self.menu_tabs.find_element_by_id('tab-4')
			self.quality_tab = self.menu_tabs.find_element_by_id('tab-5')
			self.summary_tab = self.menu_tabs.find_element_by_id('tab-6')
			# self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			pass
		return False

	def load_tabs(self):
		self.tabs = {}
		# Find elements w/ class 'tab-name'
		tabs = self.driver.find_elements_by_class_name('RRT__tab')
		for tab in tabs:
			name = tab.text.lower()
			self.tabs[name] = tab

	def selected_tab(self):

		for tabName, element in self.tabs.iteritems():
			classes = element.get_attribute('class')
			if 'RRT__tab--selected' in classes:
				return tabName

	def select_tab(self, tabName):
		try:
			tab = self.tabs[tabName.lower()]
			tab.click()

			WDW(self.driver, 10).until(lambda x: self.load(tabName))
			return True
		except KeyError:
			print('fullHealthView: No tab named: ' + str(tabName))

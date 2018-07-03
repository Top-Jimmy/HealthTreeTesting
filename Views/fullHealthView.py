from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError
from Components import fullHealthMyelomaForm
from Components import menu
from Components import header
from Views import view

class FullHealthView(view.View):

	def load(self, expectedTab=None):
		try:
			# Crap on left
			self.menu_tabs = self.driver.find_element_by_class_name('RRT__tabs')
			self.fullHealthMyelomaForm = fullHealthMyelomaForm.FullHealthMyelomaForm(self.driver)
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)

			self.selectedTab = self.selected_tab()
			if expectedTab and expectedTab != self.selectedTab:
				print('Full Health Profile: Expected state: "' + expectedTab + '", got state: "' + self.selectedTab + '"')
			else: 
				if expectedTab == 'My Myeloma':
					self.fullHealthMyelomaForm = fullHealthMyelomaForm.FullHealthMyelomaForm(self.driver)
				elif expectedTab == 'Demographics':
					self.healthDemoForm = healthDemoForm.HealthDemoForm(self.driver)
				elif expectedTab == 'Full Health History':
					self.healthHistForm = healthHistForm.HealthHistForm(self.driver)
				elif expectedTab == 'Family History':
					self.famHistForm = famHistform.FamHistform(self.driver)
				elif expectedTab == 'Lifestyle':
					self.healthLifestyleForm = healthLifestyleForm.HealthLifestyleForm(self.driver)
				elif expectedTab == 'Quality of Life':
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
			return False

	def selected_tab(self):
		self.menu_items = []
		tabs = self.menu_tabs.find_elements_by_class_name('RRT__tab')
		for i, tab in enumerate(tabs):
			classes = tab.get_attribute('class')
			if 'RRT__tab--selected' in classes:
				self.menu_items.append(tabs[i].text)

		print(self.menu_items)
	
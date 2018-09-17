from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError
from Components import fullHealthMyelomaForm, healthDemoForm, healthHistForm, famHistForm, healthLifestyleForm, healthQualityForm, healthSummaryForm
from Components import menu
from Components import header
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as AC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class FullHealthView(view.View):

	def load(self, expectedTab=None):
		try:
			# Crap on left
			self.menu_tabs = self.driver.find_element_by_class_name('RRT__tabs')

			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)


			self.load_tabs()
			self.selectedTab = self.selected_tab()
			if expectedTab and expectedTab != self.selectedTab:
				print('Full Health Profile: Expected state: "' + str(expectedTab) + '", got state: "' + str(self.selectedTab) + '"')

			else:
				if expectedTab == 'my myeloma':
					self.form = fullHealthMyelomaForm.FullHealthMyelomaForm(self.driver)
				elif expectedTab == 'demographics':
					self.form = healthDemoForm.HealthDemoForm(self.driver)
				elif expectedTab == 'full health history':
					self.form = healthHistForm.HealthHistForm(self.driver)
				elif expectedTab == 'family history':
					self.form = famHistForm.FamHistForm(self.driver)
				elif expectedTab == 'lifestyle':
					self.form = healthLifestyleForm.HealthLifestyleForm(self.driver)
				elif expectedTab == 'quality of life':
					self.form = healthQualityForm.HealthQualityForm(self.driver)
				else:
					self.form = healthSummaryForm.HealthSummaryForm(self.driver)
				self.loadedData = self.form.sections

			self.myeloma_tab = self.menu_tabs.find_element_by_id('tab-0')
			self.demographics_tab = self.menu_tabs.find_element_by_id('tab-1')
			self.health_history_tab = self.menu_tabs.find_element_by_id('tab-2')
			self.family_history_tab = self.menu_tabs.find_element_by_id('tab-3')
			self.lifestyle_tab = self.menu_tabs.find_element_by_id('tab-4')
			self.quality_tab = self.menu_tabs.find_element_by_id('tab-5')
			self.summary_tab = self.menu_tabs.find_element_by_id('tab-6')


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
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			return True
		except KeyError:
			print('fullHealthView: No tab named: ' + str(tabName))

	def submit(self, formInfo, tabName):
		# Loop through each section set in the info passed in
		for sectionIndex, section in enumerate(formInfo):
			print('answering section: ' + str(sectionIndex))
			# set loadedSection to equal a specific section[i] from the form loaded
			loadedSection = self.loadedData[sectionIndex]
			# Loop through each question in the section
			for questionIndex, question in enumerate(section):
				print('answering question: ' + str(questionIndex))
				# set loadedQuestion to equal a specific question[i] in a section[i] from the form loaded
				loadedQuestion = loadedSection[questionIndex]

				# question refers to each question passed in the formInfo
				secondaryInfo = question.get('secondary', None)
				# loadedQuestion refers to each question loaded from the form
				questionOptions = loadedQuestion.get('options', None)
				# the following 3 values are set to the actual element
				textarea = loadedQuestion.get('textInput', None)
				dropdowns = loadedQuestion.get('dropdowns', None)
				multipleDropdown = question.get('multiple_dropdown')

				if questionOptions:
					inputEl = questionOptions[question['option']]
					inputEl.click()

				if textarea:
					textarea.send_keys(question.get('textInput', None))

				if dropdowns:
					if multipleDropdown:
						self.form.set_dropdown(dropdowns[0], question.get('multiple_dropdown', None))
						AC(self.driver).send_keys(Keys.ESCAPE).perform()
					else:
						self.form.set_dropdown(dropdowns[0], question.get('dropdown', None))

				if secondaryInfo: # Question has secondary response
					# Reload question and get loadedInfo for secondary question
					WDW(self.driver, 20).until(lambda x: self.load(tabName))
					loadedSecondaryInfo = self.loadedData[sectionIndex][questionIndex].get('secondary_questions', None)

					secondaryText = secondaryInfo.get('text', None)
					secondaryOptions = secondaryInfo.get('options', None)
					if secondaryText:
						textInput = loadedSecondaryInfo[0]['textInput']
						if textInput:
							textInput.clear()
							textInput.send_keys(secondaryText)
						else:
							print('could not find textarea for question[' + str(questionIndex) + ']')
					else:
						radioOptions = loadedSecondaryInfo[0]['options']
						radioOptions[secondaryOptions].click()


				time.sleep(1)
		return True


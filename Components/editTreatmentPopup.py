from Components import datePicker
from Components import sideEffectsForm
from utilityFuncs import UtilityFunctions

import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as AC

# Form for editing outcomes/side effects

class EditTreatmentPopup():

	def __init__(self, driver):
		self.driver = driver
		self.util = UtilityFunctions(self.driver)

	def load(self, expectedValues=None):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.container = self.driver.find_element_by_class_name('editroll') # Should only 1 on T&O view
		self.buttons = self.container.find_elements_by_class_name('green-hvr-bounce-to-top')
		return self.validate(expectedValues)

	def validate(self, expectedValues):
		self.failures = []

		# Basic validation
		if len(self.buttons) != 2:
			self.failures.append('editTreatmentPopup: Expected 2 buttons, loaded ' + str(len(self.buttons)))
		if self.util.get_text(self.buttons[0]) != 'CANCEL':
			self.failures.append('editTreatmentPopup: Unexpected text on cancel button: ' + self.util.get_text(self.buttons[0]))
		if self.util.get_text(self.buttons[1]) != 'SAVE':
			self.failures.append('editTreatmentPopup: Unexpected text on save button: ' + self.util.get_text(self.buttons[1]))

		if expectedValues:
			print('editTreatmentPopup: Need to validate expectedValues')

		if len(self.failures) > 0:
			for failure in self.failures:
				print(failure)
			return False
		return True

	def parse_select_all(self, questionInfo, questionCont):
		done = False
		count = 0
		raw_input('questionInfo: ' + str(questionInfo))
		while not done and count < 5:
			try:
				# Select options in specified in optionInfo
				# De-selecting options not contained in optionInfo
				name_checker = ['Severity of the side effects', 'Cost of the treatment', 'Too much travel']
				radios = questionCont.find_elements_by_class_name('radio')
				suboption_filter = [] # Add index of any suboptions radio buttons to this list. Skip over them
				for i, radio in enumerate(radios):
					if i not in suboption_filter:
						inputs = radio.find_elements_by_tag_name('input')
						spans = radio.find_elements_by_tag_name('span')
						if len(inputs) == 0:
							print('EditTreatmentForm: radio option has no inputElements?')
						elif len(spans) == 0:
							print('EditTreatmentForm: radio option has no spanElements?')

						optionName = self.util.get_text(spans[0])
						print('optionName: ' + optionName)
						optionInput = inputs[0]
						optionInfo = questionInfo.get(optionName, False)
						raw_input('optionInfo: ' + str(optionInfo))
						subOptions = False
						if optionInfo != False: # select input, enter comment, check for subquestions
							if not optionInput.is_selected():
								raw_input('about to click option')
								self.util.click_radio(optionInput)
								raw_input('clicked option?')
							self.util.set_input(radio, optionInfo.get('comment', ''))

							# Check for suboptions or select-all
							subOptions = optionInfo.get('options', False)
							if not subOptions:
								subOptions = optionInfo.get('select-all', False)
						else:
							# De-select, clear comment, update inputs (might have hidden subquestions)
							if optionInput.is_selected():
								raw_input('de-selecting option')
								self.util.click_radio(optionInput)
								raw_input('de-selected?')
								self.util.set_input(radio, '')
								inputs = radio.find_elements_by_tag_name('input')

						# Don't iterate over suboptions
						if len(inputs) > 1:
							for inputIndex, inputEl in enumerate(inputs):
								if inputIndex > 0:
									print('skipping ' + str(i + inputIndex))
									suboption_filter.append(i + inputIndex)

						if subOptions: 
								self.parse_select_all(subOptions, radio)
				done = True
			except StaleElementReferenceException:
				print('failed to parse select-all: ' + str(count))
			count += 1
			time.sleep(.2)
		if count == 5:
			print('EditTreatmentPopup: failed to parse select-all')

	def parse_complex(self, complexInfo, questionCont):
		# For questions w/ multiple sections (sideEffects, chemotherapy drugs, medications added/removed)
		# Loop through complexInfo and select given options for each category
		# De-select options not contained in complexInfo

		# Wait for categories to show up
		categories = None
		loaded = False
		count = 0
		while not loaded and count < 5: # Doesn't immediately load
			categories = questionCont.find_elements_by_class_name('col-md-6')
			if categories:
				loaded = True
			else:
				time.sleep(.2)
			count += 1
		
		question = {}
		for i, category in enumerate(categories):
			# Has issues loading category name sometimes.
			# Make sure it's loaded before looking for options
			loadedCategoryName = False
			count = 0
			while not loadedCategoryName and count < 5:
				try:
					categoryName = self.util.get_text(category.find_element_by_class_name('treatment-group'))
					loadedCategoryName = True
				except NoSuchElementException:
					categoryName = None

				if categoryName: # Loaded name! Parse through category options
					categoryOptions = complexInfo.get(categoryName, False)
					options = {}
					for radio in category.find_elements_by_class_name('radio'):

						inputs = radio.find_elements_by_tag_name('input')
						labels = radio.find_elements_by_tag_name('label')
						label = labels[0]							

						optionName = self.util.get_text(label)
						optionInput = label.find_element_by_tag_name('input')
						optionInfo = False
						if categoryOptions:
							optionInfo = categoryOptions.get(optionName, False)
						if optionInfo != False: # select input, enter comment/intensity
							if not optionInput.is_selected():
								self.util.click_radio(optionInput)
							self.util.set_input(radio, optionInfo.get('comment', ''))
							self.set_intensity(radio, optionInfo.get('intensity', None))
						else:
							# De-select, clear comment, update inputs (might have hidden subquestions)
							if optionInput.is_selected():
								self.util.click_radio(optionInput)
								self.util.set_input(radio, '')
								inputs = radio.find_elements_by_tag_name('input')

				else: # Failed to find categoryName
					count += 1
					time.sleep(.2)

		if complexInfo.get('date', None):
			print('complex question has date. Need to set it')

	def set_intensity(self, container, value):
		try:
			sliderEl = container.find_element_by_class_name('rc-slider-handle')
		except NoSuchElementException:
			print('SideEffectsForm: failed to load sliderEl')
		curValue = sliderEl.get_attribute('aria-valuenow')

		# Need to change intensity value?
		if value != curValue:
			xOffset = None # Every time offset doesn't work, increase by 5 and try again
			additionalOffset = 0
			while str(curValue) != str(value) and additionalOffset < 50:
				if curValue != 1: # reset to base position
					AC(self.driver).drag_and_drop_by_offset(sliderEl, -200, 0).perform()

				# Calculate offset
				# Note: monitor and window sizes affect this.
				if xOffset != None:
					# First offset wasn't correct. Increment amount of offset
					additionalOffset += 4
				xOffset = 11*(value - 1) + additionalOffset
				AC(self.driver).drag_and_drop_by_offset(sliderEl, xOffset, 0).perform()
				curValue = sliderEl.get_attribute('aria-valuenow')

	def set_input(self, container, value):
		# Return if able to set value into textarea or input in container.
		try:
			textareaEl = container.find_element_by_tag_name('textarea')
			textareaEl.clear()
			textareaEl.send_keys(value)
			return True
		except NoSuchElementException:

			try:
				inputEl = container.find_element_by_tag_name('input')
				if inputEl.get_attribute('type') == 'text':
					inputEl.clear()
					inputEl.send_keys(value)
				return True
			except NoSuchElementException:
				return False

	def edit_treatment(self, newInfo, popupType, action='save'):
		# Submit info
		if popupType == 'side effects':
			self.parse_complex(newInfo['options'], self.container)
		elif popupType == 'outcomes':
			self.parse_select_all(newInfo['options'], self.container)

		# Save or cancel
		if action == 'save':
			self.util.click_el(self.buttons[1])
		elif action == 'cancel':
			self.util.click_el(self.buttons[0])
		WDW(self.driver, 15).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		return True

	
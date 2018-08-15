from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException,
		InvalidElementStateException, WebDriverException)

import time

class UtilityFunctions():
	def __init__(self, driver):
		self.driver = driver

	def set_input(self, element, value):
		# Get input/textarea el out of element
		inputEl = self.find_input(element)

		# Wait for input to be editable (displayed and enabled)
		if inputEl:
			setValue = False
			count = 0
			while not setValue and count < 5:
				try:
					inputEl.clear()
					inputEl.send_keys(value)
					if inputEl.get_attribute('value') == value:
						setValue = True
					else:
						print('SetInput: Expected "' + value + '", loaded "' + str(inputEl.get_attribute('value') + '"'))
				except InvalidElementStateException:
					print('SetInput: InvalidElementStateException')
				if not setValue:
					time.sleep(.2)
					count += 1
		else:
			print('SetInput: Could not find inputEl.')
			raise WebDriverException('SetInput: Could not find inputEl.')

	def find_input(self, element):
		inputEl = None
		tag_name = element.tag_name
		print('tag_name: ' + str(tag_name))
		if tag_name == 'input' or tag_name == 'textarea':
			inputEl = element
		else:
			# See if element contains input/textarea
			try:
				inputEl = element.find_element_by_tag_name('textarea')
			except NoSuchElementException:
				# print('SetInput: no textarea')
				try:
					inputEl = element.find_element_by_tag_name('input')
					if inputEl.get_attribute('type') != 'text':
						print('SetInput: Found input, but type is not text (may not be an issue)')
				except NoSuchElementException:
					# print('SetInput: no input')
					pass
		return inputEl

	def click_el(self, element):
		# Ensure element is clicked
		clicked = False
		count = 0
		while not clicked and count < 5:
			if self.click(element):
				clicked = True
			else:
				print('ClickEl: Tried to click element: ' + str(count))
			time.sleep(.2)
			count += 1

		if not clicked:
			print('ClickEl: Failed to click element')
			raise WebDriverException('ClickEl: Failed to click element.')

	def click_radio(self, radioEl):
		# Ensure element is clicked and selected state changed
		originalState = radioEl.is_selected()
		print('originalState: ' + str(originalState))
		newState = None

		clicked = False
		count = 0
		while not clicked and count < 5:
			if self.click(radioEl):
				clicked = True
				newState = radioEl.is_selected()
				print('newState: ' + str(newState))
			else:
				print('ClickRadio: Tried to click radioEl: ' + str(count))
			time.sleep(.2)
			count += 1

		if not clicked:
			print('ClickRadio: Failed to click radioEl.')
			raise WebDriverException('ClickRadio: Failed to click radioEl.')
		elif clicked and originalState == newState:
			print('ClickRadio: Failed to change state of radioEl')
			raw_input('?')
			raise WebDriverException('ClickRadio: Failed to change state of radioEl.')

	def click(self, element):
		try:
			element.click()
			return True
		except WebDriverException:
			print('WebDriverException: failed to click element')
		except StaleElementReferenceException:
			print('StaleElementReferenceException: failed to click element')
		return False
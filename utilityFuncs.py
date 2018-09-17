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
		if tag_name == 'input' or tag_name == 'textarea':
			return element
		else:
			# See if element contains input/textarea
			try:
				inputEl = element.find_element_by_tag_name('textarea')
			except NoSuchElementException:
				# print('SetInput: no textarea')
				try:
					inputEl = element.find_element_by_tag_name('input')
					if inputEl.get_attribute('type') != 'text':
						print('FindInput: Found input, but type is not text (may not be an issue)')
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
		changed = False
		changedCount = 0
		while not changed and changedCount < 5:

			# Ensure element is clicked and selected state changed
			originalState = radioEl.is_selected()
			# print('originalState: ' + str(originalState))
			newState = None

			clicked = False
			clickedCount = 0
			while not clicked and clickedCount < 5:
				if self.click(radioEl):
					clicked = True
					newState = radioEl.is_selected()
					# print('newState: ' + str(newState))
				else:
					print('ClickRadio: Tried to click radioEl: ' + str(clickedCount))
				time.sleep(.2)
				clickedCount += 1

			if not clicked:
				print('ClickRadio: Failed to click radioEl.')
				raise WebDriverException('ClickRadio: Failed to click radioEl.')
			elif clicked and originalState == newState:
				print('ClickRadio: Tried to change state of radioEl: ' + str(changedCount))
				
			elif clicked and originalState != newState:
				changed = True
			time.sleep(.2)
			changedCount += 1
				
		if not changed:
			raw_input('Failed to change radio?')
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

	def get_text(self, element):
		try:
			text = element.text
			text = text.strip()
			# remove single quotes, apostrophes, etc
			text = text.replace(u"\u2018", '').replace(u"\u2019", '').replace("'", '')

			# Check for extra spaces (picking up tooltip text)
			if '   ' in text:
				index = text.find('   ')
				text = text[:index]

			# Option #2: Get innerHTML of element and get first bit of react text -->text<!--
				
		except NoSuchElementException:
			print('NoSuchElementException: no element or incorrect element passed in')
			return False
		return text


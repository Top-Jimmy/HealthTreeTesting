from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver import ActionChains as AC
import time

# Component for specifying side effects when adding/editing a treatment

class SideEffectsForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self, expectedValues=None):
		print('loading sideEffectsForm')
		self.container = self.driver.find_element_by_id('sideEffectsScroll')
		self.sectionContainers = self.container.find_elements_by_class_name('new-treatment-dynamic')
		# Should be 10 sections
		if len(self.sectionContainers) != 10:
			print('SideEffectsForm: Less than 10 sections: ' + str(len(self.sectionContainers)))

		self.sections = {}
		for section in self.sectionContainers:
			self.load_section(section)

		buttons = self.container.find_elements_by_tag_name('button')
		self.save_treatment_button_top = buttons[1]
		self.cancel_button = buttons[0]
		self.save_treatment_button_bottom = buttons[2]

		self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []

		# Check for sections called 'Test Label'
		for section in self.sections:
			if section == 'test label':
				pass

		if expectedValues:
			# if self.firstname_input.get_attribute('value') != expectedValues['first_name']:
			# 	failures.append('SideEffectsForm: Expecting first name "' + expectedValues['first_name'] + '", got "' + self.firstname_input.get_attribute('value') + '"')
			pass
		if len(failures) > 0:
			for failure in failures:
				print(failure)
			raise NoSuchElementException('Failed to load SideEffectsForm')

	def load_section(self, sectionContainer):
		# Use text of section header as key (i.e. Digestive System)
		try:
			key = sectionContainer.find_element_by_class_name('treatment-group').text.lower()
		except NoSuchElementException:
			key = None

		radioContainers = sectionContainer.find_elements_by_class_name('radio')
		options = {}
		for radioCont in radioContainers:
			label = radioCont.find_element_by_tag_name('label')
			# Will have scale if option is selected
			try:
				scaleCont = radioCont.find_element_by_class_name('severity-indv-sld')
				scale = scaleCont.find_element_by_class_name('rc-slider-handle')
				scaleVal = scale.get_attribute('aria-valuenow')
				# todo: handle reading value out of scale
				# todo: handle setting value on scale
			except NoSuchElementException:
				scaleVal = None

			# Save option name (key) and inputEl (value) in options dict
			# radioCont will contain treatment scale (when visible)
			optionName = label.text.lower()
			optionInput = label.find_element_by_tag_name('input')
			options[optionName] = {
				'inputEl': optionInput,
				'container': radioCont,
			}


		if key:
			self.sections[key] = options
		else:
			print('SideEffectsForm: Failed to find header for side effects section')


################## Test functions #################

	def set(self, formInfo):
		# formInfo should be follow format in form_info.py (sideEffects)
		sideEffectValues = formInfo.get('sideEffects', None)
		if sideEffectValues is None:
			sideEffectValues = formInfo
		for sectionName in sideEffectValues:
			self.set_section(sideEffectValues[sectionName], self.sections[sectionName])

	def set_section(self, sectionInfo, loadedSectionInfo):
		# Set values in sectionInfo
		for suboption, value in sectionInfo.iteritems():
			# Grab inputEl and make sure it's selected
			try:
				inputEl = loadedSectionInfo[suboption]['inputEl']
			except KeyError:
				print('failed to load sideEffect named: ' + str(suboption))
			if not inputEl.is_selected():
				inputEl.click()

			# Set intensity
			self.set_intensity(loadedSectionInfo[suboption]['container'], value)


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
				print('additionalOffset: ' + str(additionalOffset))
				if curValue != 1: # reset to base position
					AC(self.driver).drag_and_drop_by_offset(sliderEl, -200, 0).perform()

				# Calculate offset
				# Note: monitor and window sizes affect this.
				if xOffset != None:
					# First offset wasn't correct. Increment amount of offset
					additionalOffset += 5
				xOffset = 11*(value - 1) + additionalOffset
				AC(self.driver).drag_and_drop_by_offset(sliderEl, xOffset, 0).perform()
				curValue = sliderEl.get_attribute('aria-valuenow')


# todo: reconfigure,

# 1. load should only grab section containers.
# 2. Validate should check right # of inputs per form/section?
# 3. validate should only check in-detail section headers if expectedValues dictates





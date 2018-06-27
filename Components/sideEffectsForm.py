from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

# Component for specifying side effects when adding/editing a treatment

class SideEffectsForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self, expectedValues=None):
		self.container = self.driver.find_element_by_id('sideEffectsScroll')
		self.sectionContainers = self.container.find_elements_by_class_name('new-treatment-dynamic')
		# Should be 10 sections
		if len(self.sectionContainers) != 10:
			print('SideEffectsForm: Less than 10 sections: ' + str(len(self.sectionContainers)))

		self.sections = {}
		for section in self.sectionContainers:
			self.load_section(section)

		self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
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
			optionName = label.text.lower()
			optionInput = label.find_element_by_tag_name('input')
			options[optionName] = optionInput

		if key:
			self.sections[key] = options
		else:
			print('SideEffectsForm: Failed to find header for side effects section')

	# def get_section_index(self, sectionName):
	# 	# Given name of section (i.e. 'Digestive System'), return index in loaded info (self.sections)
	# 	for i, section in enumerate(self.sections):
	# 		for key, value in section.iteritems(): # (i.e. 'digestive system', {'constipation': inputEl, 'decreased appetite': inputEl, etc...} )
	# 			if key == sectionName.lower():
	# 				return i


	def set(self, formInfo):
		# formInfo should be follow format in form_info.py (sideEffects)
		sideEffectValues = formInfo.get('sideEffects', None)
		if sideEffectValues is None:
			sideEffectValues = formInfo
		for sectionName in sideEffectValues:
			self.set_section(sideEffectValues[sectionName], self.sections[sectionName])

	def set_section(self, sectionInfo, loadedSectionInfo):
		# Set values in sectionInfo
		raw_input('sectionInfo: ' + str(sectionInfo))
		raw_input('loadedSectionInfo: ' + str(loadedSectionInfo))
		for suboption, value in sectionInfo.iteritems():
			raw_input('suboption: ' + str(suboption))
			raw_input('value: ' + str(value))







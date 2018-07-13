import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class HealthDemoForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		
		self.load_sections()
		self.save_button = self.form.find_element_by_tag_name('button')
		# print('sections: ' + str(self.sections))

		# self.validate()
		return True

	def load_sections(self):
		self.sections = []
		self.sectionContainers = self.form.find_element_by_class_name('after-head-row')
		self.rows = self.sectionContainers.find_elements_by_class_name('row')
		print('# rows: ' + str(len(self.rows)))
		for row in self.rows:
			self.sections.append(self.load_questions(row))

	def load_questions(self, row):
		rowInfo = {}
		questionList = []
		questionIndex = None
		questionConts = row.find_elements_by_class_name('cls_survey_question')
		for i, question in enumerate(questionConts):
			questionInfo = {}
			if i == 0: # Grab the question number for the index
				labels = question.find_elements_by_tag_name('label')
				index = labels[0].text.find('.')
				questionIndex = labels[0].text[:index]
			options = {}
			radioContainers = question.find_elements_by_class_name('dynamic-radio') # Container with the text (span) and input
			dropdownContainers = question.find_elements_by_class_name('Select-control')
			if dropdownContainers:
				questionInfo['dropdown'] = dropdownContainers[0]
			if radioContainers:
				for radioCont in radioContainers:
					inputs = radioCont.find_elements_by_tag_name('input')
					spans = radioCont.find_elements_by_tag_name('span')
					optionName = spans[0].text
					options[optionName] = inputs[0]

			if len(radioContainers) == 0 and len(dropdownContainers) == 0: # Non-dropdown inputs
				cityInput = question.find_element_by_tag_name('input')
				questionInfo['city'] = cityInput

			if options:
				questionInfo['options'] = options

			questionList.append(questionInfo)

			if questionIndex == None:
				print('i: ' + str(i))

		rowInfo[questionIndex] = questionList

		return rowInfo

	# def validate(self):
	# 	failures = []
	# 	if expectedValues:
	# 		if expectedValues['race'] == 'white' and not self.race_white_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expected "white" for race')
	# 		elif expectedValues['race'] == 'American Indian' and not self.race_amer_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expected "American Indian for race')
	# 		elif expectedValues['race'] == 'asian' and not self.race_asian_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expected "asian" for race')
	# 		elif expectedValues['race'] == 'black' and not self.race_black_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expected "black" for race')
	# 		elif expectedValues['race'] == 'native' and not self.race_native_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expected "native" for race')

	# 		if expectedValues['ethnicity'] == 'not Hispanic' and not self.ethn_hispanicno_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expected "not Hispanic" for ethnicity')
	# 		elif expectedValues['ethnicity'] == 'Hispanic' and not self.ethn_hispanicyes_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expected "Hispanic for ethnicity')

	# 		if self.city_born_input.get_attribute('value') != expectedValues['city_born']:
	# 			failure.append('HealthDemoForm: Expecting city where born "' + expectedValues['city_born'] + '", got "' + self.city_born_input.get_attribute('value') + '"')

	# 		if self.city_grow_input.get_attribute('value') != expectedValues['city_grow']:
	# 			failure.append('HealthDemoForm: Expecting city where grew up "' + expectedValues['city_grow'] + '", got "' + self.city_grow_input.get_attribute('value') + '"')

	# 		if self.city_adult_input.get_attribute('value') != expectedValues['city_adult']:
	# 			failure.append('HealthDemoForm: Expecting city where you live "' + expectedValues['city_adult'] + '", got "' + self.city_adult_input.get_attribute('value') + '"')

	# 		if expectedValues['health_ins'] == 'no' and not self.health_insno_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expecting "no" to having healht insurance')
	# 		elif expectedValues['health_ins'] == 'yes' and not self.health_insyes_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expecting "yes" to having health insurance')

	# 		if expectedValues['military'] == 'no' and not self.militaryno_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expecting "no" to having served in the military')
	# 		elif expectedValues['military'] == 'yes' and not self.militaryyes_radio.get_attribute('checked'):
	# 			failure.append('HealthDemoForm: Expecting "yes" to having served in the military')

	# 	if len(failures) > 0:
	# 		print(failures)
	# 		raise NoSuchElementException('Failed to load CreateAcctForm')

	
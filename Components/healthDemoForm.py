import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class HealthDemoForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		
		self.dropdowns = self.form.find_elements_by_class_name('dynamic-text-area')
		self.load_sections()
		self.save_button = self.form.find_element_by_tag_name('button')
		raw_input('sections: ' + str(self.sections))

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

	def set_dropdown(self, cont, value):
		# find right container given index (class='Select-control')
		# conts = self.driver.find_elements_by_class_name('Select-control')
		# cont = conts[dropdownIndex]

		# Figure out if you need to click 'Select-value-label' or 'Select-placeholder' element
		dropdown_preSet = False
		try:
			dropdown_value = cont.find_element_by_class_name('Select-value-label')
			dropdown_placeholder = None
			dropdown_preSet = True
		except NoSuchElementException:
			dropdown_value = None
			dropdown_placeholder = cont.find_element_by_class_name('Select-placeholder')

		# click it
		if dropdown_preSet:
			dropdown_value.click()
		else:
			dropdown_placeholder.click()
		# load options in dropdown
		options = {}
		try:
			menu = self.form.find_element_by_class_name('Select-menu-outer')
			divs = menu.find_elements_by_tag_name('div')
			for i, div in enumerate(divs):
				if i != 0:
					options[div.text.lower()] = divs[i]
		except NoSuchElementException:
			print('Unable to find dropdown items for first diagnosis')

		# click option
		try:
			option = options[value.lower()]
			option.click()

		except (IndexError, KeyError) as e:
			print('invalid index: ' + value)
			for option in options:
				print(option)

	# def load_ethnic_background_dropdown(self):
	# 	self.ethnic_background_cont = self.dropdowns[0]

	# 	# Is value already set? Should have either value or placeholder element
	# 	self.ethnic_background_preSet = False
	# 	try:
	# 		self.ethnic_background_value = self.ethnic_background_cont.find_element_by_class_name('Select-value-label')
	# 		self.ethnic_background_placeholder = None
	# 		self.ethnic_background_preSet = True
	# 	except NoSuchElementException:
	# 		self.ethnic_background_value = None
	# 		# 'Select diagnosis' placeholder
	# 		self.ethnic_background_placeholder = self.ethnic_background_cont.find_element_by_class_name('Select-placeholder')

	# def load_ethnic_background_dropdown(self):
	# 	self.country_cont = self.dropdowns[0]

	# 	# Is value already set? Should have either value or placeholder element
	# 	self.country_preSet = False
	# 	try:
	# 		self.country_value = self.country_cont.find_element_by_class_name('Select-value-label')
	# 		self.country_placeholder = None
	# 		self.country_preSet = True
	# 	except NoSuchElementException:
	# 		self.country_value = None
	# 		# 'Select diagnosis' placeholder
	# 		self.country_placeholder = self.country_cont.find_element_by_class_name('Select-placeholder')
	
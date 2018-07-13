import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class HealthHistForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		self.sectionConts = self.form.find_elements_by_class_name('after-head-row')
		self.load_sections()
		self.save_button = self.form.find_element_by_tag_name('button')

		# self.sections = [
		# 	{'1': [
		# 		{'options': {
		# 			'yes': inputEl,
		# 			'no': inputEl,
		# 		}},
		# 		{'date': inputEl},
		# 	]},
		# ]

		# Get input for 1st section, 2st row, second question 'yes'
		# self.sections[0][1]['2']['options']['yes']

	def load_sections(self):
		self.sections = []
		for section in self.sectionConts:
			self.rows = section.find_elements_by_class_name('row')
			for row in self.rows:
				# Row contains at least 1 question, might also have 1 or more subquestion
				self.sections.append(self.load_questions(row))

	def load_questions(self, row):
		rowInfo = {} # {questionIndex: [{questionInfo1}, {questionInfo2}]}
		questionList = []
		questionIndex = None
		questionConts = row.find_elements_by_class_name('cls_survey_question')

		for i, question in enumerate(questionConts):
			questionInfo = {}
			if i == 0: # Load question index (use as key for individual questions w/in each row)
				label = question.find_element_by_tag_name('label')
				index = label.text.find('.')
				questionIndex = label.text[:index]
				# raw_input('questionIndex: ' + str(questionIndex))
			options = {}
			radioContainers = question.find_elements_by_class_name('dynamic-radio') # Div containing input and span (text)
			if len(radioContainers) == 0: # No radio buttons? Check for date input
				dataInput = question.find_element_by_tag_name('input')
				questionInfo['data'] = dataInput
			for radioCont in radioContainers:
				inputs = radioCont.find_elements_by_tag_name('input')
				spans = radioCont.find_elements_by_tag_name('span')
				optionName = spans[0].text
				options[optionName] = inputs[0]

			if options:
				questionInfo['options'] = options

			questionList.append(questionInfo)

		rowInfo[questionIndex] = questionList

		return rowInfo

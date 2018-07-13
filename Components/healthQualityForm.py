import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class HealthQualityForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		self.sectionConts = self.form.find_elements_by_class_name('after-head-row')

		self.load_sections()
		self.save_button = self.form.find_element_by_tag_name('button')
		# print('sections: ' + str(self.sections))

		# self.validate()
		return True

	def load_sections(self):
		self.sections = []
		for section in self.sectionConts:
			self.rows = section.find_elements_by_class_name('row')
			for row in self.rows:
				# Row contains at least 1 question, might also have 1 or more subquestion
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
			if radioContainers:
				for radioCont in radioContainers:
					inputs = radioCont.find_elements_by_tag_name('input')
					spans = radioCont.find_elements_by_tag_name('span')
					optionName = spans[0].text
					options[optionName] = inputs[0]
			if options:
				questionInfo['options'] = options

			questionList.append(questionInfo)

			if questionIndex == None:
				print('i: ' + str(i))

		rowInfo[questionIndex] = questionList

		return rowInfo



	
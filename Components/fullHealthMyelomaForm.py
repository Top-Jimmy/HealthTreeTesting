import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class FullHealthMyelomaForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
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
		for i, section in enumerate(self.sectionConts):
			# print('loading section: ' + str(i))
			# Contains primary and any visible secondary questions
			self.questionContainers = section.find_elements_by_class_name('ques_group_cls')
			self.subQuestionIndices = []
			questionList = []
			for questionIndex, questionContainer in enumerate(self.questionContainers):
				# print('loading question: ' + str(questionIndex))
				# Primary or secondary question?
				subquestions = questionContainer.find_elements_by_class_name('ques_group_cls')
				if len(subquestions) > 0:
					for subquestionIndex in xrange(len(subquestions)):
						subIndex = questionIndex+1 + subquestionIndex
						print('subquestion: ' + str(subIndex))
						self.subQuestionIndices.append(subIndex)

				if questionIndex not in self.subQuestionIndices:
					# Primary question
					questionList.append(self.load_questions(questionContainer))
			self.sections.append(questionList)

	def load_questions(self, questionContainer, isSecondary=False):
		question = {}
		questionIndex = None
		# First is primary. Any additional ones are secondary
		questionConts = questionContainer.find_elements_by_class_name('cls_survey_question')
		if isSecondary:
			questionConts = [questionContainer]

		for i, questionCont in enumerate(questionConts):
			textInput = None
			radioOptions = None
			options = {}
			secondary_questions = []
			if i == 0: # Primary
				try:
					# look for radio options
					radioContainers = questionCont.find_elements_by_class_name('dynamic-radio')
					for radioCont in radioContainers:
						inputs = radioCont.find_elements_by_tag_name('input')
						spans = radioCont.find_elements_by_tag_name('span')
						optionName = spans[0].text.lower()
						options[optionName] = inputs[0]
					if len(radioContainers) == 0:
						textInput = questionCont.find_element_by_tag_name('input')
				except NoSuchElementException:
					pass

				# Look for an input

			else: # secondary
				secondary_questions.append(self.load_questions(questionCont, True))
			question['container'] = questionCont
			if options:
				question['options'] = options
			if textInput:
				question['textInput'] = textInput
			if secondary_questions:
				question['secondary_questions'] = secondary_questions

		return question

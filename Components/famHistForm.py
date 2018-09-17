import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from utilityFuncs import UtilityFunctions

class FamHistForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.util = UtilityFunctions(self.driver)
		self.load(expectedValues)

	def load(self, expectedValues):
		time.sleep(1)
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
					dropdownContainers = questionCont.find_elements_by_class_name('is-clearable')
					for radioCont in radioContainers:
						inputs = radioCont.find_elements_by_tag_name('input')
						spans = radioCont.find_elements_by_tag_name('span')
						optionName = self.util.get_text(spans[0]).lower()
						options[optionName] = inputs[0]
					if dropdownContainers:
						question['dropdowns'] = dropdownContainers

					if len(radioContainers) == 0 and len(dropdownContainers) == 0:
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

	def set_dropdown(self, container, value):
	# Figure out if you need to click 'Select-value-label' or 'Select-placeholder' element
		dropdown_preSet = False
		try:
			dropdown_value = container.find_element_by_class_name('Select-value-label')
			dropdown_placeholder = None
			dropdown_preSet = True
		except NoSuchElementException:
			dropdown_value = None
			dropdown_placeholder = container.find_element_by_class_name('Select-placeholder')

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

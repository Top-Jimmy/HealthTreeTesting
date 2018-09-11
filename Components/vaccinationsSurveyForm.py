from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from utilityFuncs import UtilityFunctions

class VaccinationsSurveyForm():

	def __init__(self, driver):
		self.driver = driver
		self.util = UtilityFunctions(self.driver)

	def load(self):
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		time.sleep(1)
		self.form = self.driver.find_elements_by_tag_name('form')[1]
		buttons = self.form.find_elements_by_tag_name('button')

		self.close_button = buttons[0]
		self.save_button = buttons[1]
		self.cancel_button = buttons[2]
		self.load_form()
		self.loadedData = self.questionList

		return True

	def load_form(self):
		self.questionContainers = self.form.find_elements_by_class_name('ques_group_cls')
		self.subQuestionIndices = []
		self.questionList = []
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
				self.questionList.append(self.load_questions(questionContainer))

	def load_questions(self, questionContainer, isSecondary=False):
		question = {}
		questionIndex = None
		# First is primary. Any additional ones are secondary
		questionConts = questionContainer.find_elements_by_class_name('question')

		if isSecondary:
			questionConts = [questionContainer]

		for i, questionCont in enumerate(questionConts):
			# print('loading questionCont: ' + str(i))
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
						optionName = self.util.get_text(spans[0]).lower()
						options[optionName] = inputs[0]
					if len(radioContainers) == 0:
						textInput = questionCont.find_element_by_tag_name('input')
				except NoSuchElementException:
					pass

				# Look for an input

			else: # secondary
				# Some 'question' elements don't have questions
				if len(questionCont.find_elements_by_tag_name('input')) > 0:
					# print('loading secondary question: ' + str(i))
					secondary_questions.append(self.load_questions(questionCont, True))
			question['container'] = questionCont
			if options:
				question['options'] = options
			if textInput:
				question['textInput'] = textInput
			if secondary_questions:
				question['secondary_questions'] = secondary_questions
		# print('returning: ' + str(question))
		return question

	def submit(self, mrdInfo, action='cancel'):
		for questionIndex, question in enumerate(mrdInfo):
			print('answering question: ' + str(questionIndex))
			loadedQuestion = self.loadedData[questionIndex]

			secondaryInfo = question.get('secondary', None)
			questionOptions = loadedQuestion.get('options', None)
			textarea = loadedQuestion.get('textInput', None)
			dropdowns = loadedQuestion.get('dropdowns', None)
			multipleDropdown = question.get('multiple_dropdown')

			if questionOptions:
				WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
				inputEl = questionOptions[question['option']]
				inputEl.click()
				if not inputEl.is_selected():
					print('Clicked input, but it is not selected')
					return False

			if textarea:
				textarea.send_keys(question.get('textInput', None))

			if dropdowns:
				if multipleDropdown:
					self.form.set_dropdown(dropdowns[0], question.get('multiple_dropdown', None))
					AC(self.driver).send_keys(Keys.ESCAPE).perform()
				else:
					self.form.set_dropdown(dropdowns[0], question.get('dropdown', None))

			if secondaryInfo: # Question has secondary response
				# Reload question and get loadedInfo for secondary question
				WDW(self.driver, 20).until(lambda x: self.load())
				loadedSecondaryInfo = self.loadedData[questionIndex].get('secondary_questions', None)

				secondaryText = secondaryInfo.get('text', None)
				secondaryOptions = secondaryInfo.get('options', None)
				if secondaryText:
					print(loadedSecondaryInfo)
					textInput = loadedSecondaryInfo[0]['textInput']
					if textInput:
						textInput.clear()
						textInput.send_keys(secondaryText)
					else:
						print('could not find textarea for question[' + str(questionIndex) + ']')
				else:
					radioOptions = loadedSecondaryInfo[0]['options']
					radioOptions[secondaryOptions].click()


			time.sleep(1)
		if action == 'save':
			self.save_button.click()
		else:
			self.cancel_button.click()
		return True









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
		self.sections = self.form.find_elements_by_class_name('after-head-row')
	# 	self.load_sections()

	# def load_sections(self):
	# 	self.sections = []
	# 	for section in self.sections:
	# 		questionConts = section.find_elements_by_class_name('question')
	# 		questionConts = questionConts[::2] # Every question has an empty question div after it
	# 		for questionCont in questionConts:
	# 			self.sections.append(self.load_question(questionCont))

	# def load_question(self, questionCont):
	# 	question = {}
	# 	radioContainers = section.find_elements_by_tag_name('label') # Contains label and input
	# 	# Load question info. Make sure radio option isn't a subquestion
	# 	subquestion_filter = []
	# 	for i, container in radioContainers:
	# 		if i == 0:
	# 			# 1st label is question text
	# 			questionName = container.text
	# 		else:
	# 			print('loading question: ' + str(i))
	# 			if i not in subquestion_filter:
	# 				raw_input('test moved into non-subquestion filter')
	# 				inputs = container.find_element_by_tag_name('input')
	# 				raw_input('inputs loaded')
	# 				spans = container.find_element_by_tag_name('span')
	# 				raw_input('inputs and spans loaded')

	# 				#Test Validation
	# 				if len(inputs) == 0:
	# 					print('FullHealthMyelomaForm: radio option has no inputElements?')
	# 				elif len(spans) == 0:
	# 					print('FullHealthMyelomaForm: radio option has no spanElements?')

	# 				# Get option name.
	# 				optionName = spans[0].text
	# 				print(spans[0].text)
	# 				# Check for textarea
	# 				try:
	# 					textareaEl = container.find_element_by_tag_name('textarea')
	# 				except NoSuchElementException:
	# 					textareaEl = None

	# 				subquestions = None
	# 				if len(inputs) > 1:
	# 					raw_input('test moved into subquestions')
	# 					for inputIndex, inputEl in enumerate(inputs):
	# 						if inputIndex > 0:

	# 							# Add subquestion to filter list
	# 							subquestion_filter.append(i + inputIndex)

	# 							# Load subquestion info
	# 							subquestions = self.load_question(radioContainers[i])

	# 				if textareaEl or subquestions:
	# 					question[optionName] = {
	# 						'element': inputs[0],
	# 						'textareaEl': textareaEl,
	# 						'subquestions': subquestions,
	# 					}
	# 				else:
	# 					question[optionName] = inputs[0]
	# 	elif len(datepickerContainers) > 0: # Datepicker
	# 		question['datepicker'] = datepickerContainers[0].find_element_by_tag_name('input')

	# 	return question

		#Find sections
		#Within sections find questions
		#Within questions, filter out every other question
			# questionDivs = container.find_elements_by_class_name('')
			# questions = questionDivs[::2]

		#

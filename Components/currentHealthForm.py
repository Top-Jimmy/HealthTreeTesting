import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilityFuncs import UtilityFunctions

class CurrentHealthForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.util = UtilityFunctions(self.driver)
		self.load(expectedValues)

	def load(self, expectedValues):

		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		self.question_elements = self.form.find_elements_by_class_name('custom-current-health')
		self.questions = []
		for i, question in enumerate(self.question_elements):
			self.load_question(self.question_elements[i])

		tooltips = self.form.find_elements_by_tag_name('img')
		self.blood_pressure_tooltip = tooltips[0]
		self.blood_clot_tooltip = tooltips[1]
		self.neuropathy_tooltip = tooltips[2]

		self.continue_button = self.form.find_element_by_class_name('submitForm')
		self.validate(expectedValues)
		return True

	def load_question(self, container):
		# Load question title (label), value, and any secondary questions and their values
		labels = container.find_elements_by_tag_name('label')
		question_label = self.util.get_text(labels[0])
		value = None
		secondaryQuestions = []

		# Value: None if not set
		options = ['yes', 'no', 'dont know']
		for i, label in enumerate(labels):
			if i > 0 and i < 4:
				classes = label.get_attribute('class')
				if 'active' in classes:
				 	value = options[i - 1]
		# Find secondary questions
		if value == 'yes':
			secondary_container = container.find_element_by_class_name('custom-history_label')
			secondary_questions = container.find_elements_by_class_name('form-check')

			for secondary_question in secondary_questions:
				secondary_label = self.util.get_text(secondary_question)
				secondary_input = secondary_question.find_element_by_tag_name('input')

				selected = secondary_input.is_selected()

				secondaryQuestions.append({secondary_label: selected})

		question = {
			'name': question_label,												# name: Kidney Conditions
			'value': value,																# value: 'yes'
			'secondaryQuestions': secondaryQuestions, 		# secondaryQuesitons: [
		} 																								# {'Mild kidney problems (renal impairment)': False},
		self.questions.append(question)										# {'Severe kidney problems or on dialysis': False},]

	def validate(self, expectedValues):
		failures = []
		if expectedValues:

			# meta validation
			try:
				meta_validators = expectedValues['meta']
				for key, value in meta_validators.iteritems():
					if key == 'num_questions' and value != len(self.questions):
						failures.append('CurrentHealthForm Meta: Expected ' + str(value) + ' questions. Form has ' + str(len(self.questions)))
			except KeyError:
				# No meta validation
				pass

			# Form validation
			# expectedValues should be dictionary containing {'questions': []}
			expectedQuestions = None
			try:
				expectedQuestions = expectedValues['questions']
			except KeyError:
				# No form validation
				pass
			if expectedQuestions:
				# Check # of questions match
				if len(expectedQuestions) != len(self.questions):
					failures.append('CurrentHealthForm: Expecting ' + str(len(expectedQuestions)) + ' questions. Loaded '
						+ str(len(self.questions)))
				else:
					# Each key in each expectedQuestion (secondaryQuestions, name, value) should exist in loadedQuestion and match it's value
					for i, expectedQuestion in enumerate(expectedQuestions):
						loadedQuestion = self.questions[i]
						# print('comparing ' + str(i) + ': ' + str(expectedQuestion))
						# print('with ' + str(loadedQuestion))
						# raw_input('?')
						for key, expectedValue in expectedQuestion.iteritems():
							try:
								if loadedQuestion[key] != expectedValue:
									failures.append('CurrentHealthForm: Question ' + str(i) + ' expected value "'
										+ expectedValue + '". Loaded "' + loadedQuestion[key] + '"')
							except (TypeError, KeyError) as e:
								# raw_input(str(self.questions[i]))
								failures.append('CurrentHealthForm: Expected Key "' + key + '". Not found in question ' + str(i))

		if len(failures) > 0:
			for failure in failures:
				print(failure)
			raise NoSuchElementException('Failed to load CurrentHealthForm')

	def submit(self, questionInfo, action):
		try:
			questionInfo = questionInfo['questions']
		except KeyError:
			pass

		results = []
		for i, question in enumerate(questionInfo):
			print('answering question: ' + str(i))
			results.append(self.answer_question(i, question))

		if action == 'submit':
			self.continue_button.click()
		return True

	def answer_question(self, index, questionInfo):
		container = self.question_elements[index]
		labels = container.find_elements_by_tag_name('label')
		question_label = self.util.get_text(labels[0])
		labelIndex = {'yes': 1, 'no': 2, 'dont know': 3}

		# If right question, set value
		if question_label == questionInfo['name']:
			i = labelIndex[questionInfo['value']]
			labels[i].click()

			# Handle setting any secondary questions
			if questionInfo['value'] == 'yes' and questionInfo['secondaryQuestions']:
				expectedSecondaryInfo = questionInfo['secondaryQuestions']
				secondary_container = container.find_element_by_class_name('custom-history_label')
				secondary_questions = container.find_elements_by_class_name('form-check')

				# Check # of secondary questions
				if len(secondary_questions) != len(questionInfo['secondaryQuestions']):
					print('CurrentHealth question "' + str(index) + '" expects ' + str(len(questionInfo['secondaryQuestions']))
						+ '. Loaded ' + str(len(secondary_questions)))
					return False

				# Set value for each secondary question
				for i, question in enumerate(secondary_questions):
					question_name = self.util.get_text(question)
					input_el = question.find_element_by_tag_name('input')
					print(input_el)

					if input_el.is_selected() != expectedSecondaryInfo[i][question_name]:
						self.util.click_radio(input_el)
					# else:
					# 	print(str(index) + ' already has correct value')

		else:
			print('Index "' + str(index) + '": Expecting ' + question_label + ' to equal ' + questionInfo['name'])
			return False
		return True

	def tooltip(self):
		p = self.form.find_elements_by_class_name('tooltip-p')
		self.blood_pressure_tooltip.click()
		if self.util.get_text(p[0]).lower() != 'blood pressure is the pressure exerted on walls of the blood vessels by circulating blood. along with body temperature, respiratory rate, and pulse rate, blood pressure is one of the four main vital signs monitored by medical professionals.':
			print('tooltip not clicked correctly:' + str(self.util.get_text(p[0]).lower()))
			return False

		self.blood_clot_tooltip.click()
		if self.util.get_text(p[1]).lower() != 'deep vein thrombosis (dvt) occurs when a blood clot (thrombus) forms in one or more of the deep veins in your body, usually in your legs. deep vein thrombosis can cause leg pain or swelling, but also can occur with no symptoms.':
			print('tooltip not clicked correctly:' + str(self.util.get_text(p[1]).lower()))
			return False
			
		self.neuropathy_tooltip.click()
		if self.util.get_text(p[2]).lower() != 'neuropathy is gradual onset of numbness, prickling or tingling in your feet or hands, which can spread upward into your legs and arms.':
			print('tooltip not clicked correctly:' + str(self.util.get_text(p[2]).lower()))
			return False
		return True





from Components import datePicker
from Components import sideEffectsForm
from utilityFuncs import UtilityFunctions

import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as AC

# Form for adding a treatment from 'Treatments & Outcomes' page

class EditTreatmentForm():

	def __init__(self, driver):
		self.driver = driver
		self.util = UtilityFunctions(self.driver)

	def load(self, expectedValues=None):
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.load_question_containers()
		return self.validate(expectedValues)

	def load_question_containers(self):
		self.question_containers = self.driver.find_elements_by_class_name('new-ques-div')

	def validate(self, expectedValues):
		if expectedValues:
			pass

		return True

	def validate_form(self, expectedInfo):
		failures = []

		num_questions = expectedInfo.get('num_questions', None)
		if num_questions:
			if num_questions != len(self.question_containers):
				failures.append('EditTreatmentForm: Expected ' + str(num_questions) + ' questions. Loaded ' + str(len(self.question_containers)))
			else:
				print('EditForm: correct # questions')

		if len(failures) > 0:
			for failure in failures:
				print(failure)
			raise Exception('Failed to validate EditTreatmentForm')

	def get_state(self, question):
		# Is question 'static', 'editable', or 'editing'
		state = 'static'
		editButton = None
		actionButtons = None
		try:
			# Edit question button?
			editButton = question.find_element_by_class_name('edit-module-btn')
			state = 'editable'
		except NoSuchElementException:
			# Green Action buttons? (save, cancel)
			actionButtons = question.find_elements_by_class_name('green-hvr-bounce-to-top')
			state = 'editing'

		return {'state': state, 'editButton': editButton, 'actionButtons': actionButtons}

	def open_and_edit_question(self, questionInfo):
		# Make sure question is in edit mode, then apply info from questionInfo
		questionIndex = questionInfo['index']
		print('editing question[' + str(questionIndex) + ']')
		question = self.question_containers[questionIndex]
		questionEls = self.get_state(question)
		if questionEls['state'] == 'static':
			print('unable to change static question[' + str(questionIndex) + ']')
			return False
		elif questionEls['state'] == 'editable':
			self.util.click_el(questionEls['editButton'])
			# Reload questions to avoid staleException
			self.load_question_containers()
			questionCont = self.question_containers[questionIndex]

		self.edit_question(questionCont, questionInfo)
		if questionIndex == -2:
			print('questioninfo: ' + str(questionInfo))
			raw_input('properly set?')

	def edit_question(self, questionCont, questionInfo):
		# Question should already be in edit mode
		options = questionInfo.get('options', None)
		selectAll = questionInfo.get('select-all', None)
		date = questionInfo.get('date', None)
		text = questionInfo.get('text', None)
		complexOptions = questionInfo.get('complex', None)
		if options:
			self.parse_select_all(options, questionCont)
		elif selectAll:
			self.parse_select_all(selectAll, questionCont)
		elif date:
			self.set_date(date, questionCont)
		elif text:
			self.util.set_input(questionCont, text)
		elif complexOptions:
			self.parse_complex(complexOptions, questionCont)
		else:
			print('Did not set question (could not find any info)')
		self.save_question(questionCont)

	def save_question(self, question):
		buttons = question.find_elements_by_class_name('green-hvr-bounce-to-top')
		if len(buttons) == 1:
			raw_input('should have 2 buttons')
		elif len(buttons) == 0:
			raw_input('no buttons in question?')
		elif len(buttons) == 2:
			save_button = buttons[-1]
			self.util.click_el(save_button)
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			return True

	def parse_select_all(self, questionInfo, questionCont):
		print('parse select-all')
		# Select options in specified in optionInfo
		# De-selecting options not contained in optionInfo
		name_checker = ['Severity of the side effects', 'Cost of the treatment', 'Too much travel']
		radios = questionCont.find_elements_by_class_name('radio')
		print('# radios: ' + str(len(radios)))
		suboption_filter = [] # Add index of any suboptions radio buttons to this list. Skip over them
		for i, radio in enumerate(radios):
			if i not in suboption_filter:
				print('radio: ' + str(i))
				inputs = radio.find_elements_by_tag_name('input')
				spans = radio.find_elements_by_tag_name('span')
				if len(inputs) == 0:
					print('EditTreatmentForm: radio option has no inputElements?')
				elif len(spans) == 0:
					print('EditTreatmentForm: radio option has no spanElements?')


				optionName = spans[0].text
				print(optionName)
				optionInput = inputs[0]
				optionInfo = questionInfo.get(optionName, False)
				subOptions = False
				print('optionInfo: ' + str(optionInfo))
				if optionInfo != False: # select input, enter comment, check for subquestions
					if not optionInput.is_selected():
						self.util.click_radio(optionInput)
					self.util.set_input(radio, optionInfo.get('comment', ''))

					# Check for suboptions or select-all
					subOptions = optionInfo.get('options', False)
					if not subOptions:
						subOptions = optionInfo.get('select-all', False)
				else:
					# De-select, clear comment, update inputs (might have hidden subquestions)
					if optionInput.is_selected():
						self.util.click_radio(optionInput)
						self.util.set_input(radio, '')
						inputs = radio.find_elements_by_tag_name('input')
				print('subOptions: ' + str(subOptions))
				print('inputs: ' + str(len(inputs)))

				# Don't iterate over suboptions
				if len(inputs) > 1:
					for inputIndex, inputEl in enumerate(inputs):
						if inputIndex > 0:
							print('skipping ' + str(i + inputIndex))
							suboption_filter.append(i + inputIndex)

				if subOptions: 
						self.parse_select_all(subOptions, radio)
			else:
				print('skipped radio: ' + str(i))

	def parse_complex(self, complexInfo, questionCont):
		# For questions w/ multiple sections (sideEffects, chemotherapy drugs, medications added/removed)
		# Loop through complexInfo and select given options for each category
		# De-selecting options not contained in complexInfo
		categories = questionCont.find_elements_by_class_name('new-treatment-dynamic')
		question = {}
		for i, category in enumerate(categories):
			# Has issues loading category name sometimes.
			# Make sure it's loaded before looking for options
			loadedCategoryName = False
			count = 0
			while not loadedCategoryName and count < 5:
				try:
					categoryName = category.find_element_by_class_name('treatment-group').text
					loadedCategoryName = True
				except NoSuchElementException:
					categoryName = None
				# print('categoryName: ' + str(categoryName))
				if categoryName: # Loaded name! Parse through category options
					categoryOptions = complexInfo.get(categoryName, False)
					# print('categoryOptions: ' + str(categoryOptions))
					options = {}
					for radio in category.find_elements_by_class_name('radio'):

						inputs = radio.find_elements_by_tag_name('input')
						labels = radio.find_elements_by_tag_name('label')
						label = labels[0]							

						optionName = label.text
						optionInput = label.find_element_by_tag_name('input')
						optionInfo = False
						if categoryOptions:
							optionInfo = categoryOptions.get(optionName, False)
						if optionInfo != False: # select input, enter comment/intensity
							if not optionInput.is_selected():
								self.util.click_radio(optionInput)
							self.util.set_input(radio, optionInfo.get('comment', ''))
							self.set_intensity(radio, optionInfo.get('intensity', None))
						else:
							# De-select, clear comment, update inputs (might have hidden subquestions)
							if optionInput.is_selected():
								self.util.click_radio(optionInput)
								self.util.set_input(radio, '')
								inputs = radio.find_elements_by_tag_name('input')

				else: # Failed to find categoryName
					count += 1
					time.sleep(.2)

		if complexInfo.get('date', None):
			print('complex question has date. Need to set it')
		# raw_input('properly set?')

	def set_date(self, date, question):
		picker = datePicker.DatePicker(self.driver, question.find_element_by_class_name('new-datepicker'))
		dateSet = False
		count = 0
		while not dateSet and count < 3:
			try:
				picker.set_date(date)
				dateSet = True
			except (ElementNotVisibleException, StaleElementReferenceException, ValueError, KeyError) as e:
				time.sleep(.4)
			count += 1
		if count == 3:
			print('Failed to set date')

	def set_intensity(self, container, value):
		if value:
			try:
				sliderEl = container.find_element_by_class_name('rc-slider-handle')
			except NoSuchElementException:
				print('EditTreatmentForm: failed to load sliderEl')
			curValue = sliderEl.get_attribute('aria-valuenow')

			# Need to change intensity value?
			if value != curValue:
				xOffset = None # Every time offset doesn't work, increase by 5 and try again
				additionalOffset = 0
				while str(curValue) != str(value) and additionalOffset < 50:
					if curValue != 1: # reset to base position
						AC(self.driver).drag_and_drop_by_offset(sliderEl, -200, 0).perform()

					# Calculate offset
					# Note: monitor and window sizes affect this.
					if xOffset != None:
						# First offset wasn't correct. Increment amount of offset
						additionalOffset += 4
					xOffset = 11*(value - 1) + additionalOffset
					AC(self.driver).drag_and_drop_by_offset(sliderEl, xOffset, 0).perform()
					curValue = sliderEl.get_attribute('aria-valuenow')

	def leave_form(self):
		buttons = self.driver.find_elements_by_class_name('green-hvr-bounce-to-top')
		back_button = buttons[1]
		self.util.click_el(back_button)
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def edit_treatment(self, newTreatmentInfo):
		for i, info in enumerate(newTreatmentInfo):
			if i == 0: # 1st item should have validation info for whole form
				self.validate_form(info)
			else: # Items after 1st should be questions
				self.open_and_edit_question(info)
		self.leave_form()
		return True


######################## Treatment Metadata ############################

# Chemotherapy
		# 0: Treatment Type [0]
		# 1: Start Date [1]
		# 2: Currently taking? [2]
		# 3: End Date NA/[3]
		# 4: Maintenance therapy? [3]/[4]
		# 5: Type of chemo [4]/[5]
		# 6: Changes? [5]/[6]
			# 7: Added NA/[6]/[7]
			# 8: Removed NA/6,7,8
		# 7: Best response -2
		# 8: Side Effects -1

# Clinical
		# 0: Treatment Type [0]
		# 1: Start Date [2]
		# 2: Currently taking? [3]
		# 3: End Date NA/[4]
		# 4: NCT # [1]
		# 5: Main treatment [4]/[5]
		# 6: Best response -2
		# 7: Side Effects -1


# Extra (Bone strengtheners, Antibiotics, Antifungal)
	# Bone strengthener (edit)
		# 0: Treatment Type [0]
		# 1: Bone Strengthener Type [2]
		# 2: Start Date [3]
		# 3: Are you currently taking bone strengtheners? [4]
		# 4: End Date [5]/NA
		# 5. Frequency [5]/[6] (-1)

	# Antibiotics (edit)
		# 0: Treatment Type [0]
		# 1: Antibiotics Type [2]
		# 2: Start Date [3]
		# 3: Currently taking antibiotics? [4]
		# 4: End Date [5]/NA

	# Antifungal (edit)
		# 0: Treatment Type [0]
		# 1: Antifungal Type [2]
		# 2: Start Date [3]
		# 3: Currently taking antifungal? [4]
		# 4: End Date [5]/NA


# Radiation
		# 0: Treatment Type [0]
		# 1: Radiation type [1]
		# 2: Start Date [2]
		# 3: End Date [3]
		# 4: Best response -2
		# 5: Side Effects -1


# Stemcell (non induction)
		# 0: Treatment Type [0]
		# 1: Stemcell type [1]
		# 2: SC Start Date [3] [9] if is induction therapy (+6)
		# 3: Type of chemo [4] ('Melphalan (Alkeran)' unless q[4] was answered w/ comment)
			# 4: Dose of chemo drug (q[4] subquestion #2)
		# 5: Best response -3
		# 6: Side Effects -2

# Induction
		# 0: Treatment Type ('induction therapy')
		# 1: Induction Start Date [3]
		# 2: Still taking? [4]
		# 3: Induction end date N/A/[5]
		# 4: Type of induction therapy [5]/[6]
		# 5: Induction changes? [6]/[7]
		# 6: Induction Best response [7]/[8]
		# 7: Induction Side Effects [8]/[9]


from Components import datePicker
from Components import sideEffectsForm

import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as AC

# Form for editing outcomes/side effects

class EditTreatmentPopup():

	def __init__(self, driver):
		self.driver = driver

	def load(self, expectedValues=None):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.container = self.driver.find_element_by_class_name('editroll') # Should only 1 on T&O view
		self.buttons = self.container.find_elements_by_class_name('green-hvr-bounce-to-top')
		return self.validate(expectedValues)

	def validate(self, expectedValues):
		self.failures = []

		# Basic validation
		if len(self.buttons) != 2:
			self.failures.append('editTreatmentPopup: Expected 2 buttons, loaded ' + str(len(self.buttons)))
		if self.buttons[0].text != 'CANCEL':
			self.failures.append('editTreatmentPopup: Unexpected text on cancel button: ' + self.buttons[0].text)
		if self.buttons[1].text != 'SAVE':
			self.failures.append('editTreatmentPopup: Unexpected text on save button: ' + self.buttons[1].text)

		if expectedValues:
			print('editTreatmentPopup: Need to validate expectedValues')

		if len(self.failures) > 0:
			for failure in self.failures:
				print(failure)
			return False
		return True

	def answer_question(self, optionName, optionInfo, subOptionName=None):
		# OptionName: 'My myeloma is now undetectable'
		# optionInfo: {'I dont know the details of my response': {}}

		# Note: This function is a bit different from it's counterpart in other forms.
		# optionInfo typically contains other stuff besides subquestions. In this function it solely
		# has info related to subquestions

		comment = optionInfo.get('comment', None)
		secondaryOptions = optionInfo.get('options', None)
		raw_input('secondaryOptions: ' + str(secondaryOptions))

		# Get loaded info for given option/subOption
		try:
			loadedInfo = self.load_question(self.container)
			loadedQuestion = loadedInfo[optionName]
		except KeyError:
			print(optionName + ' not in question options')
			print('question: ' + str(self.questions[0]))
			raise KeyError()
		if subOptionName:
			loadedQuestion = loadedQuestion['subquestions'][subOptionName]

		# Grab input element out of loadedQuestion for option/subOption
		inputEl = loadedQuestion
		optionTextarea = None
		if type(loadedQuestion) is dict:
			inputEl = loadedQuestion.get('element', None)
			optionTextarea = loadedQuestion.get('textareaEl', None)

		# Make sure option is selected
		if not inputEl.is_selected():
			inputEl.click()
			if comment or secondaryOptions:
				self.load()

		# handle comment (optional)
		if comment:
			if not optionTextarea:
				optionTextarea = self.questions[0][optionName]['textareaEl']
			optionTextarea.clear()
			optionTextarea.send_keys(optionInfo['comment'])

		# handle secondaryQuestions
		if secondaryOptions:
			for secondaryOption in secondaryOptions:
				self.answer_question(optionName, secondaryOptions[secondaryOption], secondaryOption)

	# def set_option(self, optionInfo):
	# 	# option might be string (optionName), or might be dictionary with extra info (comment text)
	# 	questionInfo = self.load_question(self.container)
	# 	optionName = optionInfo
	# 	comment = None
	# 	if type(optionInfo) == dict:
	# 		# {'Other': {'comment': 'Radiation treatment Y'}}
	# 		for name, info in optionInfo.iteritems():
	# 			optionName = name
	# 			comment = info.get('comment', None)
	# 	inputEl = questionInfo.get(optionName, None)
	# 	if type(inputEl) is dict:
	# 		# get inputEl if questionInfo[optionName] has extra info
	# 		inputEl = inputEl['element']
	# 	if inputEl and not inputEl.is_selected():
	# 		inputEl.click()
	# 	else:
	# 		print('Question does not have option: ' + str(optionInfo))

	# 	if comment:
	# 		textarea = self.container.find_element_by_tag_name('textarea')
	# 		textarea.clear()
	# 		textarea.send_keys(comment)

	def load_question(self, container):
		# Load outcomes question
		# radioCont = container.find_element_by_class_name('col-md-12')
		radios = container.find_elements_by_class_name('radio')
		questionInfo = {}
		subquestion_filter = [] # Add index of any subquestion radio buttons to this list
		for i, radio in enumerate(radios):
			if i not in subquestion_filter: # Don't load info if current radio option is a subquestion
				inputs = radio.find_elements_by_tag_name('input')
				spans = radio.find_elements_by_tag_name('span')

				# Test Validation
				if len(inputs) == 0:
					print('EditTreatmentPopup: radio option has no inputElements?')
				elif len(spans) == 0:
					print('EditTreatmentPopup: radio option has no spanElements?')

				# Get option name.
				optionName = spans[0].text
				optionName.replace("'", '')
				# Check for textarea
				try:
					textareaEl = radio.find_element_by_tag_name('textarea')
				except NoSuchElementException:
					textareaEl = None

				# handle any subquestions
				subquestions = None
				if len(inputs) > 1: # All inputs after 1st should be secondary questions
					for inputIndex, inputEl in enumerate(inputs):
						if inputIndex > 0:

							# Add subquestion to filter list
							subquestion_filter.append(i + inputIndex)

							# Load subquestion info
							subquestions = self.load_question(radios[i])

				# Pass back dict if loaded anything besides inputElement
				# todo: handle passing back secondary questions
				if textareaEl or subquestions:
					questionInfo[optionName] = {
						'element': inputs[0],
						'textareaEl': textareaEl,
						'subquestions': subquestions,
					}
				else:
					questionInfo[optionName] = inputs[0]
		return questionInfo

	def set_complex(self, newOptions, container):
		# For questions w/ multiple sections (sideEffects, chemotherapy drugs, medications added/removed)
		categories = container.find_elements_by_class_name('new-treatment-dynamic')
		question = {}
		for i, category in enumerate(categories):

			# Has issues loading category name sometime.
			# Make sure it's loaded before looking for options
			loadedCategoryName = False
			count = 0
			while not loadedCategoryName and count < 5:
				try:
					categoryEl = category.find_element_by_class_name('treatment-group')
					categoryName = categoryEl.text.lower()
				except NoSuchElementException:
					categoryName = None

				if categoryName:
					print('categoryName: ' + str(categoryName))
					loadedCategoryName = True

					# Does newOptions have any in this category?
					changesToCategory = False
					newCategoryOptions = newOptions.get(categoryName, None)
					if newCategoryOptions:
						changesToCategory = True

					radioContainers = category.find_elements_by_class_name('radio')
					options = {}
					for radioCont in radioContainers:
						label = radioCont.find_element_by_tag_name('label')


						# Save option name (key) and inputEl (value) in options dict
						# radioCont will contain treatment scale or textarea (when visible)
						optionName = label.text.lower()
						optionInput = label.find_element_by_tag_name('input')

						if not changesToCategory:
							# Make sure every option in category is de-selected
							if optionInput.is_selected():
								optionInput.click()
						else:
							# Check if this option needs to be selected
							newOption = newCategoryOptions.get(optionName, '')
							# Should be {} (has option) or {'intensity': x} (has option and need to set intensity)
							if newOption != '':
								# Has this option. Select it and set intensity (if applicable)
								if not optionInput.is_selected():
									optionInput.click()

								# Handle setting sideEffects
								if newOption.get('intensity', None):
									hasIntensity = False

									self.set_intensity(radioCont, newOption['intensity'])
							else:
								# Doesn't have option. Make sure it's not selected
								if optionInput.is_selected():
									optionInput.click()

				else:
					count += 1
					time.sleep(.2)
					# raw_input('failed to find category name: ' + str(count))

			# print('count: ' + str(count))
				# raw_input('failed to find category name')

		# Check if question has datepicker (added chemotherapy medications question)
		try:
			datepickerCont = container.find_element_by_class_name('mnth-datepicker')
			question['datepicker'] = datepickerCont
		except NoSuchElementException:
			# Complex question does not have datepicker
			pass

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
		try:
			sliderEl = container.find_element_by_class_name('rc-slider-handle')
		except NoSuchElementException:
			print('SideEffectsForm: failed to load sliderEl')
		curValue = sliderEl.get_attribute('aria-valuenow')

		# Need to change intensity value?
		if value != curValue:
			xOffset = None # Every time offset doesn't work, increase by 5 and try again
			additionalOffset = 0
			while str(curValue) != str(value) and additionalOffset < 50:
				# print('additionalOffset: ' + str(additionalOffset))
				if curValue != 1: # reset to base position
					AC(self.driver).drag_and_drop_by_offset(sliderEl, -200, 0).perform()

				# Calculate offset
				# Note: monitor and window sizes affect this.
				if xOffset != None:
					# First offset wasn't correct. Increment amount of offset
					additionalOffset += 5
				xOffset = 11*(value - 1) + additionalOffset
				AC(self.driver).drag_and_drop_by_offset(sliderEl, xOffset, 0).perform()
				curValue = sliderEl.get_attribute('aria-valuenow')

	def edit_treatment(self, newInfo, popupType, action='save'):
		# Submit info
		raw_input('editing treatment')
		if popupType == 'side effects':
			self.set_complex(newInfo['complex'])
		elif popupType == 'outcomes':
			options = newInfo['options']
			for key in options:
				self.answer_question(key, options[key])
			# self.set_option(newInfo['options'])

		# Save or cancel
		if action == 'save':
			self.buttons[1].click()
		elif action == 'cancel':
			self.buttons[0].click()
		WDW(self.driver, 15).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		raw_input('done editing treatment')

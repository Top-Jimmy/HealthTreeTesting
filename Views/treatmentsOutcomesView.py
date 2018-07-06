from viewExceptions import MsgError, WarningError
from Components import addTreatmentForm
from Components import menu
from Components import header
from Components import popUpForm
from Views import view

from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TreatmentsOutcomesView(view.View):
	post_url = 'about-me'

	# self.treatment_questions = {
	# 	'radiation': ['treatment', 'treatmentType', 'startDate', 'endDate', 'outcome'],
	# 	'bogus': 'bogus',
	# }

	def load(self, expectedValues=None, expectedState=None):
		try:
			WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			self.state = self.load_state()
			if expectedState and expectedState != self.state:
				print('Wrong state! Expected ' + str(expectedState) + ', got ' + str(self.state))

			if self.state == 'fresh':
				# load new popup
				# todo: need new account to get this state
				pass
			else:
				buttonCont = self.driver.find_element_by_class_name('custom1-add-treatment-btn')
				self.add_treatments_button = buttonCont.find_elements_by_tag_name('button')[0]
				if self.state == 'saved':
					self.saved_test_containers = self.driver.find_elements_by_class_name('custom-seperator')
			return self.validate(expectedValues)
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			print('found error')
			return False

	def load_state(self):
		# New user gets popup asking whether they have received treatments before (yes/no)
		# Todo: figure out how to load popup

		# Saved treatment?
		try:
			savedTable = self.driver.find_element_by_class_name('custom-seperator')
			return 'saved'
		except NoSuchElementException:
			# normal?
			try:
				buttonCont = self.driver.find_element_by_class_name('custom1-add-treatment-btn')
				return 'normal'
			except NoSuchElementException:
				return 'fresh'

	def validate(self, expectedValues):
		failures = []

		if self.state == 'fresh':
			# todo: Validate text on 'fresh' popup
			pass
		else:
			if self.add_treatments_button and self.add_treatments_button.text != 'Add Treatments':
				failures.append('treatmentsOutcomesView: Unexpected text on add treatment button')
			if self.state == 'saved':
				if expectedValues:
					# Verify tests have expected data
					expectedTests = expectedValues.get('test', expectedValues)
					for testIndex, test in enumerate(expectedTests):

						# pull data out of test container
						savedData = self.read_test(testIndex)
						expectedQuestions = expectedTests['questions']
						expectedSideEffects = expectedTests['sideEffects']


						for i, question in enumerate(expectedQuestions):
							expectedValue = ''
							try:
								savedValue = savedData[radiation_questions[i]]
							except KeyError:
								print('KeyError: ' + str(radiation_questions[i]))

				# 'startDate': startDate,
				# 'endDate': endDate,
				# 'type': therapyType,
				# 'treatments': treatments,
				# 'sideEffects': sideEffects,
				# 'outcome': outcomeStr,
				# 'testIndex': index,

					pass
				elif self.state == 'normal':
					pass

		if len(failures) > 0:
			for failure in failures:
				print(failure)
				raise NoSuchElementException("Failed to load treatmentsOutcomesView")
		else:
			return True

	def read_test(self, index):
		cont = self.saved_test_containers[testIndex]
		rows = cont.find_elements_by_class_name('data-row')
		divs = rows[0].find_elements_by_tag_name('div')
		uls = rows[0].find_elements_by_tag_name('ul')

		startDate = divs[0].text
		endDate = divs[1].text
		treatment = divs[2].text # i.e. radiation, stem cell, etc

		# Not sure this should be a list. Possible to have multiple treatmentTypes?
		treatmentTypes = [] # treatment type
		treatmentItems = uls[0].find_element_by_tag_name('li')
		for li in treatmentItems:
			treatmentTypes.append(li.text)

		sideEffects = {}
		sideEffectItems = uls[1].find_elements_by_tag_name('li')
		for li in sideEffectItems:
			sideEffect = li.find_element_by_class_name('side_effect_li').text
			intensity = li.find_element_by_class_name('side_effect_severity').text
			sideEffects[sideEffect] = intensity

		outcomeStr = rows[1].find_elements_by_tag_name('div')[1].text

		return {
			'startDate': startDate, # 'Oct 2017'
			'endDate': endDate,
			'treatment': treatment, # 'radiation'
			'treatmentType': treatmentTypes, # 'total body radiation'
			'sideEffects': sideEffects, # {'blood clots': 9, 'irregular/rapid heartbeat': 4}
			'outcome': outcomeStr, # 'I discontinued this treatment because: Cost of the treatment, Too much travel.'
			'testIndex': index,
		}

	def add_treatment(self, treatmentInfo, action='submit', expectedError=None, expectedWarnings=None):
		try:
			# print(self.state)
			if self.state == 'normal' or self.state == 'saved':
				self.add_treatments_button.click()
				self.addTreatmentForm = addTreatmentForm.AddTreatmentForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.addTreatmentForm.load())
				if self.addTreatmentForm.add_treatment(treatmentInfo):
					WDW(self.driver, 10).until(lambda x: self.load(expectedState='saved'))
				else:
					print('Failed to add treatment')

			else:
				# todo: handle fresh popup
				pass
			return True
		except MsgError:
			# Is add treatment expected to fail?
			errorType = self.error['errorType']
			if expectedError and errorType.lower() == expectedError.lower():
				return True
			print(self.error['errorMsg'])
			if errorType == 'undefined':
				print('Undefined error: ' + self.error['errorText'])
		except WarningError:
			# Is form submission expected to have warning?
			unexpectedWarnings = []
			if expectedWarnings:
				# Go through self.warnings and check each warningType matches an expectedWarning
				# Append warnings that aren't expected to unexpectedWarnings
				for i, warning in enumerate(self.warnings):
					expected = False
					warningType = warning['type']
					for expectedWarning in expectedWarnings:
						if expectedWarning == warningType:
							expected = True
					if not expected:
						unexpectedWarnings.append(self.warnings[i])

				if unexpectedWarnings:
					for unexpected in unexpectedWarnings:
							print(unexpected['msg'])
							if warningType == 'undefined':
								print('Undefined warning: ' + unexpected['text'])
				else:
					return True
		return True

	def edit(self, treatmentIndex, editType, newInfo):
		if self.state == 'saved':
			table = self.saved_test_containers[treatmentIndex]
			actionRow = table.find_element_by_class_name('bottom-last-row')
			actions = self.load_actions(actionRow)

			try:
				action = actions[editType]
				action.click()
			except KeyError:
				print(str(editType) + ' Is not a valid treatment option')
				raise KeyError('Not a valid treatment optino')

			if editType == 'delete':
				self.popUpForm = popUpForm.PopUpForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
				self.popUpForm.confirm(newInfo)
			# elif editType == 'treatments':
				# pass

			self.load()

	def load_actions(self, actionRow):
		links = actionRow.find_elements_by_tag_name('a')
		if len(links) != 4:
			print('Unexpected # links in treatment table: ' + str(len(links)))

		return {
			'treatments': links[0],
			'outcomes': links[1],
			'sideEffects': links[2],
			'delete': links[3],
		}







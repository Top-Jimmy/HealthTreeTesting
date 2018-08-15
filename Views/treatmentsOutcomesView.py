from viewExceptions import MsgError, WarningError
from Components import addTreatmentForm
from Components import editTreatmentForm
from Components import editTreatmentPopup
from Components import menu
from Components import header
from Components import popUpForm
from Components import newAccountPopUpForm
from Views import view
from utilityFuncs import UtilityFunctions

import time
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, WebDriverException, TimeoutException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TreatmentsOutcomesView(view.View):
	post_url = 'about-me'

	def load(self, expectedValues=None, expectedState=None):
		try:
			WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			self.util = UtilityFunctions(self.driver)
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			self.state = self.load_state()
			self.tutorial_button = self.driver.find_element_by_class_name('videobtn')
			if expectedState and expectedState != self.state:
				print('Wrong state! Expected ' + str(expectedState) + ', got ' + str(self.state))
				return False
			if self.state == 'fresh':
				self.newAccountPopUpForm = newAccountPopUpForm.NewAccoutPopUpForm(self.driver)
				# load new popup
				# todo: need new account to get this state
				pass
			else:
				self.tutorial_button = self.driver.find_element_by_class_name('videobtn')
				try:
					self.view_options_button = self.driver.find_element_by_class_name('treatment_op_btn')
				except NoSuchElementException:
					self.view_options_button = None
				self.load_add_treatment_button()
				self.saved_tests = self.driver.find_elements_by_class_name('table_container')
			return self.validate(expectedValues)
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def load_state(self):
		# New user gets popup asking whether they have received treatments before (yes/no)
		# Todo: figure out how to load popup

		# Saved treatment?
		try:
			savedTable = self.driver.find_element_by_class_name('outer-mypataient-table')
			return 'saved'
		except NoSuchElementException:
			# normal?
			try:
				buttonCont = self.driver.find_element_by_class_name('custom1-add-treatment-btn')
				return 'normal'
			except NoSuchElementException:
				return 'fresh'

	def load_add_treatment_button(self):
		buttonCont = self.driver.find_element_by_class_name('custom1-add-treatment-btn')
		self.add_treatments_button = buttonCont.find_elements_by_tag_name('button')[0]

	def validate(self, expectedValues):
		self.failures = []

		if expectedValues:
			print('validating expectedValues')
			meta = expectedValues.get('meta', None)
			if meta:
				for key, value in meta.iteritems():
					if key == 'num_treatments':
						if value != len(self.saved_tests):
							self.failures.append('Treatments&Outcomes Meta: Expected ' + str(value) + ' treatments. Form has ' + str(len(self.saved_tests)))
						else:
							print('correct number of treatents: ' + str(value))

			elif self.state == 'fresh':
				# todo: Validate text on 'fresh' popup
				print('validating fresh')
				pass
			else:
				if self.add_treatments_button and self.add_treatments_button.text != 'Add Treatments':
					self.failures.append('treatmentsOutcomesView: Unexpected text on add treatment button')
				if self.state == 'saved':
					print('validating saved')
					# Verify tests have expected data
					extraTypes = ['bone strengtheners', 'antibiotics', 'antifungal']
					expectedTests = expectedValues.get('tests', {})
					for testIndex, test in enumerate(expectedTests):
						print('T&O: Validating test: ' + str(testIndex))
						# Test meta data
						testType = test['testMeta']['type']
						numQuestions = len(test['questions'])

						# read data out of test's table
						# if only validating 1 test, make sure grabbing last loadedTest
						if len(expectedTests) == 1:
							testIndex = -1
						savedTest = self.read_test(testIndex)
						# raw_input('savedTest: ' + str(savedTest))
						savedData = savedTest['testData']

						if testType == 'clinical':
							self.compare_nct(savedData['nct #'], test, testType)
							self.compare_treatments(savedData['treatment type'], test, testType)
						else:
							# All other treatment types have treatments and therapy type
							self.compare_therapy_type(savedData['therapy type'], test, testType)
							self.compare_treatments(savedData['treatments'], test, testType)
						if testType == 'stem cell':
							self.compare_start_date(self.convert_date(savedData['transplant date']), test, testType)
						else:
							self.compare_start_date(self.convert_date(savedData['start date']), test, testType)
							self.compare_end_date(self.convert_date(savedData['end date']), test, testType)

						if testType in extraTypes: # Bone Strengtheners, Antibiotics, Antifungal
							self.compare_frequency(savedData['frequency'], test, testType)
						else: # Chemo, Radiation, Stem Cell
							self.compare_side_effects(savedData['side effects'], test, testType)
							self.compare_outcome(savedData['outcome'], test, testType)

				elif self.state == 'normal':
					print('validating normal')
					pass

		if len(self.failures) > 0:
			print('Failures!')
			for failure in self.failures:
				print(failure)
				raise NoSuchElementException("Failed to load treatmentsOutcomesView")
		else:
			return True

	def read_test(self, testIndex):
		# 'actions': {'treatments': webEl, 'outcomes': webEl, 'sideEffects': webEl, 'delete': webEl}
		# 'testData': {
		# 	'start date': 'Jan 2018',
		# 	'end date': 'Current Treatment',
		# 	'therapy type': 'Maintenance Therapy',
		# 	'treatments': ['melphalan', 'Adriamycin (Removed On: Mar 2018) (Reason: Drug cost)'],
		# 	'side effects': {'blood clots': {'intensity': 9}, 'irregular/rapid heartbeat': {'intensity': 2}}
		# }
		testData = {}
		treatments = []
		sideEffects = {}
		actions = {}

		cont = self.saved_tests[testIndex]
		rows = cont.find_elements_by_tag_name('tr')
		testKeys = [] # ['start date', 'end date', 'therapy type', 'treatments', 'side effects']
		for rowIndex, row in enumerate(rows):
			# Header values
			if rowIndex == 0:
				tds = row.find_elements_by_tag_name('td')
				for td in tds:
					testKeys.append(td.text.lower())

			# Test values
			elif rowIndex == 1:
				tds = row.find_elements_by_tag_name('td')
				for tdIndex, td in enumerate(tds):
					key = testKeys[tdIndex]
					if tdIndex == len(tds)-2: # Treatments List (2nd to last td)
						items = td.find_elements_by_class_name('treatments-lbl-span')
						for treatment in items:
							treatmentText = treatment.text.lower()
							treatments.append(treatmentText)
						# Clinical doesn't have items (just text)
						if not items:
							treatments.append(td.text)
						testData[key] = treatments

					elif tdIndex == len(tds)-1: # Last row: index=4 (3 for stem cell)
						# Side Effects (chemo, radiation, stem cell)
						items = td.find_elements_by_class_name('treatments-lbl-span')
						if len(items) > 0:
							for effect in items:
								name = effect.find_element_by_tag_name('span').text
								intensity = int(effect.find_element_by_tag_name('div').text)
								sideEffects[name] = {'intensity': intensity}
							testData[key] = sideEffects

						else: # Frequency (Bone strengtheners, antibiotics, antifungal)
							# Only bone strengtheners have frequency (otherwise 'N/A')
							text = td.text
							print('text: ' + str(text))
							if text:
								testData[key] = text.lower()
							else: # Might have no side effects (any type of treatment)
								testData[key] = sideEffects

					else: # Start date, end date, therapy type
						testData[key] = td.text.lower()

			# Outcome (no outcome for bone strengtheners, antibiotics, antifungal. Table only has 3 rows)
			elif rowIndex == 2 and len(rows) == 4:
				td = row.find_elements_by_tag_name('td')[1] # text is in 2nd td
				testData['outcome'] = td.text.lower()

			# Actions (last row)
			elif (rowIndex + 1) == len(rows):
				anchors = row.find_elements_by_tag_name('a')
				if len(anchors) == 4:
					actions['treatments'] = anchors[0]
					actions['outcomes'] = anchors[1]
					actions['sideEffects'] = anchors[2]
					actions['delete'] = anchors[3]
				elif len(anchors) == 2: # bone strengtheners, antibiotics, antifungal
					actions['treatments'] = anchors[0]
					actions['delete'] = anchors[1]

		# print('done loading test: ' + str(testIndex))
		return {
			'actions': actions,
			'testData': testData,
		}

	def convert_date(self, dateStr):
		# Input: 'mmm yyyy', Output; 'mm/yyyy'
		spaceIndex = dateStr.find(' ') # Should always be 3
		if spaceIndex == 3:
			months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
			monthName = dateStr[:3]
			year = dateStr[4:]

			month = str(months.index(monthName) + 1).zfill(2)
			return month + '/' + str(year)
		else:
			if dateStr != 'current treatment':
				print('Unexpected date format: ' + str(dateStr))
			return dateStr

	def parse_sideEffects(self, info):
		# {'cardiovascular/circulatory system': {
			# 'irregular/rapid heartbeat': {'intensity': 2},
			# 'blood clots': {'intensity': 9}}
		# }
		# converted to...
		# {u'irregular/rapid heartbeat': {'intensity': u'2'},
		# 	u'blood clots': {'intensity': u'9'}
		# }
		sideEffects = {}
		if info:
			for category in info:
				for effect, value in info[category].iteritems():
					sideEffects[effect] = value
		return sideEffects

	def calc_start_date(self, testType, test):
		# Stem Cell: question[3] unless it's induction therapy (question[2]=yes), then it's 8
		if testType == 'stem cell':
			index = 3
			for key in test['questions'][2]['options']:
				if key.lower() == 'yes':
					index = 8
			return index

	def compare_start_date(self, savedVal, test, testType):
		questionIndicies = {
			'stem cell': self.calc_start_date(testType, test),
			'radiation': 2,
			'chemo': 1,
			'bone strengtheners': 3,
			'antibiotics': 3,
			'antifungal': 3,
			'clinical': 2,
		}

		# Start Date (universal treatment option)
		questionIndex = questionIndicies[testType]
		expectedVal = test['questions'][questionIndex]['text']
		if savedVal != expectedVal:
			self.failures.append('T&Outcomes: Expected start date ' + str(expectedVal) + ', loaded ' + str(savedVal))
		else:
			print('correct start date')

	def compare_end_date(self, savedVal, test, testType):
		if testType == 'radiation':
			expectedVal = test['questions'][3]['text']
		elif testType == 'chemo':
			expectedVal = 'current treatment'
			if test['questions'][3]['type'] == 'date':
				expectedVal = test['questions'][3]['text']
		elif testType == 'clinical':
			expectedVal = 'current treatment'
			if test['questions'][4]['type'] == 'date':
				expectedVal = test['questions'][4]['text']
		else:
			try:
				expectedVal = test['questions'][5]['text'] # If no question[5] it's 'current treatment'
			except (IndexError, KeyError) as e:
				# No end date
				expectedVal = 'current treatment'

		if savedVal != expectedVal:
			self.failures.append('T&Outcomes: Expected end date ' + str(expectedVal) + ', loaded ' + str(savedVal))
		else:
			print('correct end date')

	def compare_therapy_type(self, savedVal, test, testType):
		if testType == 'radiation':
			expectedVal = 'radiation'
		elif testType == 'stem cell':
			expectedVal = 'stem cell transplant'
		elif testType == 'chemo':
			# If it's not maintenance therapy, ExpectedVal is option from 1st question
			# Index of maintenance therapy question depends on if treatment is 'current' or not
			expectedVal = 'current treatment'
			maintenanceIndex = 3
			if test['questions'][3]['type'] == 'date':
				# Is a current treatment. Maintenance is index 4
				maintenanceIndex = 4

			isMaintenance = False
			for key in test['questions'][maintenanceIndex]['options']:
				if key.lower() == 'yes':
					expectedVal = 'maintenance therapy'
				else:
					# Don't pull from question options. Exact text does not match
					expectedVal = 'Chemotherapy / Myeloma Therapy'.lower()
		else:
			for key in test['questions'][1]['options']:
				expectedVal = key.lower()

		if savedVal != expectedVal:
			self.failures.append('T&Outcomes: Expected therapyType ' + str(expectedVal) + ', loaded ' + str(savedVal))
		else:
			print('correct therapy type')

	def compare_side_effects(self, savedVal, test, testType):
		# Everything has sideEffects except for 'extra' treatments
		index = -1
		if testType == 'stem cell':
			index = -2
		expectedVal = self.parse_sideEffects(test['questions'][index]['options'])
		# print('expectedVal: ' + str(expectedVal))
		if savedVal != expectedVal:
			self.failures.append('T&Outcomes: Expected sideEffects ' + str(expectedVal) + ', loaded ' + str(savedVal))
		else:
			print('correct side effects')

	def compare_treatments(self, savedVal, test, testType):
		# SavedVal should be a list with all the treatment options
		expectedVal = None
		if testType == 'clinical':
			# Clinical shouldn't have multiple 'options', just text from question 4/5
			# question[4] might be stop date
			if test['questions'][4].get('type', None) == 'input':
				expectedVal = test['questions'][4].get('text', None)
			else:
				expectedVal = test['questions'][5].get('text', None)
			if expectedVal:
				expectedVal = ['Clinical Trial: ' + expectedVal]
		else:
			print('Not evaluating treatments for testType: ' + str(testType))

		if expectedVal:
			if savedVal != expectedVal:
				self.failures.append('T&Outcomes: Expected treatment ' + str(expectedVal) + ', loaded ' + str(savedVal))
			else:
				print('correct treatment')

	def compare_frequency(self, savedVal, test, testType):
		# Only for Bone strengthener, antibiotics, antifungal
		if testType == 'bone strengtheners':
			for key in test['questions'][-1]['options']:
				expectedVal = key.lower()
		else:
			expectedVal = 'na'

		if savedVal != expectedVal:
			self.failures.append('T&Outcomes: Expected frequency ' + str(expectedVal) + ', loaded ' + str(savedVal))
		else:
			print('correct frequency')

	def compare_nct(self, savedVal, test, testType):
		expectedVal = None
		if testType == 'clinical':
			expectedVal = test['questions'][1]['text'].lower()

		if expectedVal and savedVal != expectedVal:
			self.failures.append('T&Outcomes: Expected NCT# ' + str(expectedVal) + ', loaded ' + str(savedVal))
		else:
			print('correct nct')

	def compare_outcome(self, savedVal, test, testType):
		# Only for chemo, radiation, stem cell
		expectedOutcomes = []
		index = -2
		if testType == 'stem cell':
			index = -3
		options = test['questions'][index]['options']
		for optionName, value in options.iteritems():
			expectedOutcomes.append(optionName.lower())

		# 'options': {
		# 	'I discontinued this treatment': {
		# 		'type': 'select-all',
		# 		'options': {
		# 			'Too much travel': {},
		# 			'Other': {'comment': 'Discontinued comment: Treatment2'},
		# 		},
		# 	}
		if expectedOutcomes[0] == 'i discontinued this treatment':
			# There's subquestions. Get expected options for subquestion
			suboptions = options['I discontinued this treatment']['options']
			for suboption, value in suboptions.iteritems():
				expectedOutcomes.append(suboption.lower())
				# Get comment if 'other' is selected
				if suboption.lower() == 'other':
					try:
						comment = value['comment']
						expectedOutcomes.append(comment.lower())
					except AttributeError:
						print('No comment')

		hasError = False
		for expectedOutcome in expectedOutcomes:
			if not expectedOutcome in savedVal:
				self.failures.append('T&Outcomes: Expected outcome ' + str(expectedOutcome) + ', loaded ' + str(savedVal))
				hasError = True

		if not hasError:
			print('correct outcome')

############################ Utility Functions ###############################

	def delete_treatment(self):
		self.popUpForm = popUpForm.PopUpForm(self.driver)
		WDW(self.driver, 20).until(lambda x: self.popUpForm.load())
		self.popUpForm.confirm('confirm')
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def edit_treatments(self, editInfo, expectedInfo):
		self.editTreatmentForm = editTreatmentForm.EditTreatmentForm(self.driver)
		WDW(self.driver, 20).until(lambda x: self.editTreatmentForm.load())
		if self.editTreatmentForm.edit_treatment(editInfo):
			WDW(self.driver, 20).until(lambda x: self.load({'tests': [expectedInfo]}, 'saved'))

	def edit_outcomes(self, editInfo, expectedInfo):
		self.popUpEditor = editTreatmentPopup.EditTreatmentPopup(self.driver)
		WDW(self.driver, 20).until(lambda x: self.popUpEditor.load())
		if self.popUpEditor.edit_treatment(editInfo, 'outcomes'):
			WDW(self.driver, 20).until(lambda x: self.load({'tests': [expectedInfo]}, 'saved'))

	def edit_side_effects(self, editInfo, expectedInfo):
		self.popUpEditor = editTreatmentPopup.EditTreatmentPopup(self.driver)
		WDW(self.driver, 20).until(lambda x: self.popUpEditor.load())
		if self.popUpEditor.edit_treatment(editInfo, 'side effects'):
			WDW(self.driver, 20).until(lambda x: self.load({'tests': [expectedInfo]}, 'saved'))

	def load_actions(self, tableContainer):
		lastRow = tableContainer.find_elements_by_tag_name('tr')[-1]
		links = lastRow.find_elements_by_tag_name('a')
		if len(links) == 4:
			return {
				'treatments': links[0],
				'outcomes': links[1],
				'side effects': links[2],
				'delete': links[3],
			}
		elif len(links) == 2: # Bone Strengtheners, Antibiotics, Anti Fungals
			return {
				'treatments': links[0],
				'delete': links[1],
			}

	def click_add_treatment(self):
		# Sometimes thinks there's an element in the way of button
		clicked = False
		count = 0
		while not clicked and count < 5:
			# Has issues clicking for some reason. 
			try:
				buttonCont = self.driver.find_element_by_class_name('custom1-add-treatment-btn')
				button = buttonCont.find_elements_by_tag_name('button')[0]
				self.util.click_el(button)
				clicked = True
			except WebDriverException:
				print('could not click add treatment button: ' + str(count))
				time.sleep(.4)
				pass
			count += 1

		if count == 5:
			print('failed to click add treatment button')

############################### Test Functions. ####################################

	def add_treatment(self, treatmentInfo, expectedInfo=None, expectedError=None, expectedWarnings=None):
		# ExpectedInfo should be list of expected tests
		if expectedInfo is None:
			expectedInfo = [treatmentInfo]
		try:
			# print(self.state)
			if self.state == 'normal' or self.state == 'saved':
				self.click_add_treatment()
				self.addTreatmentForm = addTreatmentForm.AddTreatmentForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.addTreatmentForm.load())
				if self.addTreatmentForm.add_treatment(treatmentInfo):
					WDW(self.driver, 10).until(lambda x: self.load({'tests': expectedInfo}, 'saved'))
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

	def edit_treatment(self, treatmentIndex, editType, expectedInfo=None, editInfo=None, popupAction='confirm'):
		if self.state == 'saved':
			actions = self.load_actions(self.saved_tests[treatmentIndex])

			try:
				action = actions[editType]
				self.util.click_el(action)
			except KeyError:
				print(str(editType) + ' Is not a valid treatment option')
				raise KeyError('Not a valid treatment option')

			if editType == 'delete':
				self.delete_treatment()
			else:
				if editType == 'treatments':
					self.edit_treatments(editInfo, expectedInfo)
				elif editType == 'outcomes':
					self.edit_outcomes(editInfo, expectedInfo)
				elif editType == 'side effects':
					self.edit_side_effects(editInfo, expectedInfo)
				# self.clear_alert()
			print('Done editing: ' + str(editType))

	def delete_all_treatments(self):
		if self.state == 'saved':
			num_treatments = len(self.saved_tests)
			for i, saved_test in enumerate(self.saved_tests):
				print('deleting treatment #' + str(i))
				actions = self.load_actions(self.saved_tests[0])
				try:
					self.util.click_el(actions['delete'])
				except KeyError:
					print('"delete" Is not a valid treatment option')
					raise KeyError('Not a valid treatment option')
				self.delete_treatment()
				# Should be 1 less treatment
				WDW(self.driver, 10).until(lambda x: self.load({'meta': {'num_treatments': num_treatments - (i+1)}}))

	def view_options(self):
		if self.view_options_button:
			self.util.click_el(self.view_options_button)
			url = self.driver.current_url
			if '/treatment-options' not in url:
				return False
		else:
			print('Treatment & Outcomes view does not have "View Options" button')
			return False












from viewExceptions import MsgError, WarningError
from Components import addTreatmentForm
from Components import menu
from Components import header
from Components import popUpForm
from Components import newAccountPopUpForm
from Views import view

from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TreatmentsOutcomesView(view.View):
	post_url = 'about-me'

	def load(self, expectedValues=None, expectedState=None):
		try:
			WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			self.state = self.load_state()
			if expectedState and expectedState != self.state:
				print('Wrong state! Expected ' + str(expectedState) + ', got ' + str(self.state))
				return False
			if self.state == 'fresh':
				self.newAccountPopUpForm = newAccountPopUpForm.NewAccoutPopUpForm(self.driver)
				# load new popup
				# todo: need new account to get this state
				pass
			else:
				buttonCont = self.driver.find_element_by_class_name('custom1-add-treatment-btn')
				self.add_treatments_button = buttonCont.find_elements_by_tag_name('button')[0]
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

	def validate(self, expectedValues):
		failures = []

		if expectedValues:
			# print('validating expectedValues')
			meta = expectedValues.get('meta', None)
			if meta:
				for key, value in meta.iteritems():
					if key == 'num_treatments' and value != len(self.saved_tests):
						failures.append('Treatments&Outcomes Meta: Expected ' + str(value) + ' treatments. Form has ' + str(len(self.saved_tests)))

			elif self.state == 'fresh':
				# todo: Validate text on 'fresh' popup
				pass
			else:
				if self.add_treatments_button and self.add_treatments_button.text != 'Add Treatments':
					failures.append('treatmentsOutcomesView: Unexpected text on add treatment button')
				if self.state == 'saved':
					# Verify tests have expected data
					# raw_input('expectedValues: ' + str(expectedValues))
					extraTypes = ['bone strengtheners', 'antibiotics', 'antifungal']
					expectedTests = expectedValues.get('tests', {})
					for testIndex, test in enumerate(expectedTests):
						# Test meta data
						testType = test['testMeta']['type']
						numQuestions = len(test['questions'])

						# read data out of test's table
						# if only validating 1 test, make sure grabbing last loadedTest
						if len(expectedTests) == 1:
							testIndex = -1
						savedTest = self.read_test(testIndex)
						# raw_input('savedTEst: ' + str(savedTest))
						savedData = savedTest['testData']

						if testType == 'chemo':

							# Start date (always 2nd question)
							savedVal = self.convert_date(savedData['start date'])
							expectedVal = test['questions'][1]['text']
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected start date ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct start date')

							# End Date
							hasEndDate = False
							expectedVal = 'current treatment'
							if test['questions'][3]['type'] == 'date':
								hasEndDate = True
								expectedVal = test['questions'][3]['text']

							savedVal = self.convert_date(savedData['end date'])
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected end date ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct end date')

							# Therapy Type
							# ExpectedVal is option from 1st question, unless question 3/4 is 'yes' (then it's 'maintenance therapy')
							isMaintenance = False
							maintenanceIndex = 3 # Maintenance question is index 3, unless there is an end date
							if hasEndDate:
								maintenanceIndex = 4
							for key in test['questions'][maintenanceIndex]['options']:
								if key.lower() == 'yes':
									isMaintenance = True

							if isMaintenance:
								expectedVal = 'maintenance therapy'
							else:
								# Don't pull from question options. Exact text does not match
								expectedVal = 'Chemotherapy / Myeloma Therapy'.lower()

							savedVal = savedData['therapy type']
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected treatmentType ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct therapy')

							# sideEffects
							savedVal = savedData['side effects']
							expectedVal = self.parse_sideEffects(test['questions'][-1]['options'])
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected sideEffects ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct side effects')

						elif testType == 'radiation':
							pass

							# Start date (always question[2])
							savedVal = self.convert_date(savedData['start date'])
							expectedVal = test['questions'][2]['text']
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected start date ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct start date')

							# End Date (alwyas 4th question)
							savedVal = self.convert_date(savedData['end date'])
							expectedVal = test['questions'][3]['text']
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected end date ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct end date')

							# Treatment Type
							savedVal = savedData['therapy type']
							expectedVal = 'radiation'
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected treatmentType ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct therapy')

							# Side Effects
							savedVal = savedData['side effects']
							expectedVal = self.parse_sideEffects(test['questions'][-1]['options'])
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected sideEffects ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct side effects')

						elif testType in extraTypes:

							# Start date
							savedVal = self.convert_date(savedData['start date'])
							expectedVal = test['questions'][3]['text']
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected start date ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct start date')

							# End Date
							savedVal = self.convert_date(savedData['end date'])
							try:
								# End Date is question[5]
								expectedVal = test['questions'][5]['text']
							except (IndexError, KeyError) as e:
								# No end date
								expectedVal = 'current treatment'
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected end date ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct end date')

							# Treatment Type
							savedVal = savedData['therapy type']
							for key in test['questions'][1]['options']:
								expectedVal = key.lower()
							if savedVal != expectedVal:
								failures.append('T&Outcomes: Expected treatmentType ' + str(expectedVal) + ', loaded ' + str(savedVal))
							else:
								print('correct therapy')

				elif self.state == 'normal':
					pass

		if len(failures) > 0:
			print('Failures!')
			for failure in failures:
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
					if tdIndex == 3: # Treatments List
						items = td.find_elements_by_class_name('treatments-lbl-span')
						for treatment in items:
							treatmentText = treatment.text.lower()
							treatments.append(treatmentText)
						testData[key] = treatments

					elif tdIndex == 4:  # SideEffects List
						items = td.find_elements_by_class_name('treatments-lbl-span')
						for effect in items:
							name = effect.find_element_by_tag_name('span').text.lower()
							intensity = int(effect.find_element_by_tag_name('div').text)
							sideEffects[name] = {'intensity': intensity}

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
		for category in info:
			for effect, value in info[category].iteritems():
				sideEffects[effect] = value
		return sideEffects


############################### Test Functions. ####################################

	def add_treatment(self, treatmentInfo, expectedError=None, expectedWarnings=None):
		try:
			# print(self.state)
			if self.state == 'normal' or self.state == 'saved':
				self.add_treatments_button.click()
				self.addTreatmentForm = addTreatmentForm.AddTreatmentForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.addTreatmentForm.load())
				if self.addTreatmentForm.add_treatment(treatmentInfo):
					WDW(self.driver, 10).until(lambda x: self.load({'tests': [treatmentInfo]}, 'saved'))
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

	def edit(self, treatmentIndex, editType, newInfo=None, popupAction='confirm'):
		if self.state == 'saved':
			table = self.saved_tests[treatmentIndex]
			actions = self.load_actions(table.find_elements_by_tag_name('tr')[-1])

			try:
				action = actions[editType]
				action.click()
			except KeyError:
				print(str(editType) + ' Is not a valid treatment option')
				raise KeyError('Not a valid treatment option')

			if editType == 'delete':
				self.popUpForm = popUpForm.PopUpForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
				self.popUpForm.confirm(popupAction)

			WDW(self.driver, 10).until(lambda x: self.load(newInfo))

	def load_actions(self, lastRow):
		links = lastRow.find_elements_by_tag_name('a')
		if len(links) == 4: #
			return {
				'treatments': links[0],
				'outcomes': links[1],
				'sideEffects': links[2],
				'delete': links[3],
			}
		elif len(links) == 2: # Bone Strengtheners, Antibiotics, Anti Fungals
			return {
				'treatments': links[0],
				'delete': links[1],
			}









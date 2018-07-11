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

		if expectedValues:
			meta = expectedValues.get('meta', None)
			if meta:
					for key, value in meta.iteritems():
						if key == 'num_treatments' and value != len(self.saved_test_containers):
							failures.append('Treatments&Outcomes Meta: Expected ' + str(value) + ' treatments. Form has ' + str(len(self.saved_test_containers)))
						else:
							print('correct # of treatments')

			elif self.state == 'fresh':
				# todo: Validate text on 'fresh' popup
				pass
			else:
				if self.add_treatments_button and self.add_treatments_button.text != 'Add Treatments':
					failures.append('treatmentsOutcomesView: Unexpected text on add treatment button')
				if self.state == 'saved':
					# Verify tests have expected data
					expectedTests = expectedValues.get('test', expectedValues)
					for testIndex, test in enumerate(expectedTests):

						# pull data out of test container
						savedData = self.read_test(testIndex)
						expectedQuestions = expectedTests['questions']
						expectedSideEffects = expectedTests['sideEffects']

						# WIP
						# for i, question in enumerate(expectedQuestions):
						# 	expectedValue = ''
						# 	try:
						# 		savedValue = savedData[radiation_questions[i]]
						# 	except KeyError:
						# 		print('KeyError: ' + str(radiation_questions[i]))

				elif self.state == 'normal':
					pass

		if len(failures) > 0:
			for failure in failures:
				print(failure)
				raise NoSuchElementException("Failed to load treatmentsOutcomesView")
		else:
			return True

	def read_test(self, testIndex):
		# {

		# }

		testData = {}
		treatments = []
		sideEffects = {}
		actions = {}

		cont = self.saved_tests[testIndex]
		rows = cont.find_elements_by_tag_name('tr')
		testKeys = [] # ['start date', 'end date', 'therapy type', 'treatments', 'side effects']
		for rowIndex, row in enumerate(rows):


			if rowIndex == 0: # Header values
				tds = row.find_elements_by_tag_name('td')
				for td in tds:
					testKeys.append(td.text.lower())

			elif rowIndex == 1: # Test values
				tds = row.find_elements_by_tag_name('td')
				for tdIndex, td in enumerate(tds):
					key = testKeys[i]
					if i == 3: # Treatments List
						items = td.find_elements_by_tag_name('li')
						for treatment in items:
							treatmentText = treatment.text.lower()
							treatments.append(treatmentText)
						testData[key] = treatments

					elif i == 4:  # SideEffects List
						items = td.find_elements_by_tag_name('li')
						for sideEffect in items:
							name = td.find_element_by_tag_name('span').text.lower()
							intensity = td.find_element_by_tag_name('div').text.lower()

							sideEffects[name] = intensity
						testData[key] = sideEffects

					else: # Start date, end date, therapy type
						testData[key] = td.text.lower()

			elif rowIndex == 2: # Outcome
				td = row.find_elements_by_tag_name('td')[1] # text is in 2nd td
				testData['outcome'] = td.text.lower()

			elif rowIndex == 3: # Actions
				anchors = row.find_elements_by_tag_name('a')
				if len(anchors) == 4:
					actions['treatments'] = anchors[0]
					actions['outcomes'] = anchors[1]
					actions['sideEffects'] = anchors[2]
					actions['delete'] = anchors[3]
				elif len(anchors == 2):
					pass


		return {
			'actions': actions,
			'testData': testData,
		}


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

	def add_treatment(self, treatmentInfo, expectedError=None, expectedWarnings=None):
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

	def edit(self, treatmentIndex, editType, newInfo=None, popupAction='confirm'):
		if self.state == 'saved':
			table = self.saved_test_containers[treatmentIndex]
			actionRow = table.find_element_by_class_name('bottom-last-row')
			actions = self.load_actions(actionRow)

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
			# elif editType == 'treatments':
				# pass

			WDW(self.driver, 10).until(lambda x: self.load(newInfo))

	def load_actions(self, actionRow):
		links = actionRow.find_elements_by_tag_name('a')
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









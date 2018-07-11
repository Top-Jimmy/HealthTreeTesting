from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import menu
from Components import header
from Components import fishTestForm
from Components import gepTestForm
from Components import ngsTestForm
from Components import editHighRiskForm
from Components import popUpForm
from Components import uploadFileForm
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MyelomaGeneticsView(view.View):
	post_url = 'myeloma-genetics'

	def load(self, formInfo=None):
		try:
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)

			# When user has already filled out info
			raw_input('loading...')
			addDiagnosisButtons = self.driver.find_elements_by_class_name('addDiagnoisisButton')
			self.add_fish_button = addDiagnosisButtons[0]
			self.add_gep_button = addDiagnosisButtons[1]
			self.add_ngs_button = addDiagnosisButtons[2]

			raw_input('buttons loaded')

			buttons = self.driver.find_elements_by_tag_name('button')
			self.upload_file_button = buttons[2]

			raw_input('file button loaded')

			cont = self.driver.find_element_by_class_name('genetics-btn')
			self.continue_button = cont.find_element_by_tag_name('button')

			# self.tables = self.driver.find_elements_by_class_name('marg-btm0')
			# raw_input('all but tables loaded')
			# self.load_fish_table()
			# raw_input('fish table loaded')
			# self.load_gep_table()
			# raw_input('gep table loaded')
			# self.load_ngs_table()
			# raw_input('ngs table loaded')
			# self.load_highRisk_table()
			# raw_input('high risk table loaded')


			# When user hasn't filled anything out
				# todo

			# self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def load_fish_table(self):
		fishTable = self.tables[0]
		rows = fishTable.find_elements_by_class_name('row')

		values = [] # add text from each header row to values list
		self.fish_tests = [] # add text from test rows to dictionary (use values as keys)
		for i, row in enumerate(rows):
			# print('row ' + str(i))
			labResult = {}
			divs = row.find_elements_by_tag_name('div')
			# last 2 divs are containers for actions. Remove one of them
			if i > 0:
				del divs[-1]
			# print('# fish divs: ' + str(len(divs)))
			for divIndex, div in enumerate(divs):
				text = div.text
				# find divs in row
				# loop through divs
				if i == 0:
					# Collect column headers
					values.append(div.text)
				else:
					# print(str(divIndex))
					key = values[divIndex]
					if key.lower() == 'actions':
						actions = []
						buttons = row.find_elements_by_tag_name('button')
						actions.append(buttons[0])
						actions.append(buttons[1])
						labResult[key] = actions
					else:
						labResult[key] = text
			if labResult:
				self.fish_tests.append(labResult)

	def load_gep_table(self):
		gepTable = self.tables[1]
		rows = gepTable.find_elements_by_class_name('row')

		values = [] # add text from each header row to values list
		self.gep_tests = [] # add text from test rows to dictionary (use values as keys)
		for i, row in enumerate(rows):
			labResult = {}
			divs = row.find_elements_by_tag_name('div')
			# last 2 divs are containers for actions. Remove one of them
			# print('row ' + str(i))
			# print('# divs: ' + str(len(divs)))
			if i > 0:
				del divs[-1]
			for divIndex, div in enumerate(divs):
				text = div.text
				# find divs in row
				# loop through divs
				if i == 0:
					# Collect column headers
					values.append(div.text)
				else:
					key = values[divIndex]
						# No div for 'actions' in header.
					if key.lower() == 'actions':
						actions = []
						buttons = row.find_elements_by_tag_name('button')
						actions.append(buttons[0])
						actions.append(buttons[1])
						labResult['actions'] = actions
					else:
						labResult[key] = text
			if labResult:
				self.gep_tests.append(labResult)

	def load_ngs_table(self):
		ngsTable = self.tables[2]
		rows = ngsTable.find_elements_by_class_name('row')

		values = [] # add text from each header row to values list
		self.ngs_tests = [] # add text from test rows to dictionary (use values as keys)
		for i, row in enumerate(rows):
			labResult = {}
			divs = row.find_elements_by_tag_name('div')
			# last 2 divs are containers for actions. Remove one of them
			if i > 0:
				del divs[-1]
			# print('# divs in ngs table: ' + str(len(divs)))
			for divIndex, div in enumerate(divs):
				text = div.text
				if i == 0:
					# Collect text from column headers
					values.append(div.text)
				else:
					key = values[divIndex]
					if key.lower() == 'actions':
						actions = []
						buttons = row.find_elements_by_tag_name('button')
						actions.append(buttons[0])
						actions.append(buttons[1])
						labResult[key] = actions
					elif key != '':
						labResult[key] = text
			if labResult:
				self.ngs_tests.append(labResult)

	def load_highRisk_table(self):
		highRiskTable = self.tables[3]
		self.edit_high_risk_button = highRiskTable.find_element_by_tag_name('button')
		rows = highRiskTable.find_elements_by_class_name('row')

		values = []
		self.highRisk_tests = []
		for i, row in enumerate(rows):
			labResult = {}
			divs = row.find_elements_by_tag_name('div')
			# print('High risk: row ' + str(i) + ' has ' + str(len(divs)) + ' divs')
			for divIndex, div in enumerate(divs):

				text = div.text
				if i == 0:
					values.append(div.text)
				else:
					# Only grab 'test' and 'answer'
					if divIndex < 2:
						key = values[divIndex]
						labResult[key] = text
					# elif i == 1 and divIndex == 2:
					# 	# Only 1st test row has action button
					# 	self.edit_high_risk_button = row.find_element_by_tag_name('button')
						
				

					
				

				# if i == 0:
				# 	values.append(div.text)
				# else:
				# 	key = values[i]

				# 	if key == 'actions':
				# 		if i == 1:
				# 			raw_input('heyo')
				# 			self.high_risk_edit_button = row.find_element_by_tag_name('button')
			if labResult:
				self.highRisk_tests.append(labResult)

	def validate(self):
		failures = []
		if self.continue_button.text != 'Continue':
			failure.append('MyelomaGeneticsView: Unexpected text "' + self.continue_button.text + '"')

	# def submit(self, formInfo, expectedError=None, expectedWarnings=None):
	# 	try:
	# 		if self.aboutMeForm.enter_info(formInfo):
	# 			# Should be on myeloma diagnosis page
	# 			url = self.driver.current_url
	# 			if '/myeloma-genetics' not in url:
	# 				self.error = self.readErrors()
	# 				self.warnings = self.aboutMeForm.read_warnings()
	# 				if self.error:
	# 					raise MsgError('Login Error')
	# 				elif self.warnings:
	# 					raise WarningError('Submission warning')
	# 		return True
	# 	except MsgError:
	# 		# Is login expected to fail?
	# 		errorType = self.error['errorType']
	# 		if expectedError and errorType.lower() == expectedError.lower():
	# 			return True
	# 		print(self.error['errorMsg'])
	# 		if errorType == 'undefined':
	# 			print('Undefined error: ' + self.error['errorText'])
	# 	except WarningError:
	# 		# Is form submission expected to have warning?
	# 		unexpectedWarnings = []
	# 		if expectedWarnings:
	# 			# Go through self.warnings and check each warningType matches an expectedWarning
	# 			# Append warnings that aren't expected to unexpectedWarnings
	# 			for i, warning in enumerate(self.warnings):
	# 				expected = False
	# 				warningType = warning['type']
	# 				for expectedWarning in expectedWarnings:
	# 					if expectedWarning == warningType:
	# 						expected = True
	# 				if not expected:
	# 					unexpectedWarnings.append(self.warnings[i])

	# 			if unexpectedWarnings:
	# 				for unexpected in unexpectedWarnings:
	# 						print(unexpected['msg'])
	# 						if warningType == 'undefined':
	# 							print('Undefined warning: ' + unexpected['text'])
	# 			else:
	# 				return True
	# 	return False

	# def click_link(self, link):
	# 	if link == 'create account':
	# 		self.createAccount_link.click()
	# 	elif link == 'forgot password':
	# 		self.signInForm.forgotPassword_link.click()
	def add_fish_test(self, fishInfo, action='save'):
		self.add_fish_button.click()
		self.fishTestForm = fishTestForm.FishTestForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.fishTestForm.load())
		self.fishTestForm.submit(fishInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def add_gep_test(self, gepInfo, action='cancel'):
		self.add_gep_button.click()
		self.gepTestForm = gepTestForm.GepTestForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.gepTestForm.load())
		self.gepTestForm.submit(gepInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def add_ngs_test(self, ngsInfo, action='save'):
		self.add_ngs_button.click()
		self.ngsTestForm = ngsTestForm.NgsTestForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.ngsTestForm.load())
		self.ngsTestForm.submit(ngsInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def edit_test(self, testType, testIndex, testValues, action='delete', popUpAction='confirm'):
		test = ''
		if testType == 'fish':
			test = self.fish_tests[testIndex]
			if action == 'edit':
				test['actions'][0].click()
			else:
				test['actions'][1].click()
				self.popUpForm = popUpForm.PopUpForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
				self.popUpForm.confirm(popUpAction)
			# Load edit form
			# call submit function of edit form and pass in testValues
			# reload page and pass in testValues as expectedValues
		elif testType == 'gep':
			test = self.gep_tests[testIndex]
			if action == 'edit':
				test['actions'][0].click()
			else:
				test['actions'][1].click()
				self.popUpForm = popUpForm.PopUpForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
				self.popUpForm.confirm(popUpAction)

		elif testType == 'ngs':
			test = self.ngs_tests[testIndex]
			if action == 'edit':	
				test['actions'][0].click()
			else:
				test['actions'][1].click()
				self.popUpForm = popUpForm.PopUpForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
				self.popUpForm.confirm(popUpAction)
		else:
			self.edit_high_risk_button.click()

		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def edit_high_risk(self, riskInfo, action='save'):
		self.edit_high_risk_button.click()
		self.editHighRiskForm = editHighRiskForm.EditHighRiskForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.editHighRiskForm.load())
		self.editHighRiskForm.submit(riskInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def upload_file(self, action='cancel'):
		self.upload_file_button.click()
		self.uploadFileForm = uploadFileForm.UploadFileForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.uploadFileForm.load())
		self.uploadFileForm.confirm(action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))













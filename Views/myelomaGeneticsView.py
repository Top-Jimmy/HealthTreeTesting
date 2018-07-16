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
			addDiagnosisButtons = self.driver.find_elements_by_class_name('addDiagnoisisButton')
			self.add_fish_button = addDiagnosisButtons[0]
			self.add_gep_button = addDiagnosisButtons[1]
			self.add_ngs_button = addDiagnosisButtons[2]

			buttons = self.driver.find_elements_by_tag_name('button')
			self.upload_file_button = buttons[2]

			cont = self.driver.find_element_by_class_name('genetics-btn')
			self.continue_button = cont.find_element_by_tag_name('button')

			# self.tables = self.driver.find_elements_by_class_name('table_container')
			self.load_fish_table()
			self.load_gep_table()
			self.load_ngs_table()
			self.load_highRisk_table()


			# When user hasn't filled anything out
				# todo

			# self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def load_fish_table(self):
		self.fish_tests = []
		fishTable = self.driver.find_element_by_id('fish_table')
		rows = fishTable.find_elements_by_class_name('table_row')
		labInfo = [] # add text from each header row to values list
		for rowIndex, row in enumerate(rows):
			labResult = {}
			divs = row.find_elements_by_tag_name('div')
			tds = row.find_elements_by_tag_name('td')
			# for divIndex, div in enumerate(divs):
			for tdIndex, td in enumerate(tds):
				if rowIndex == 0:
					labInfo.append(td.text.lower())
				else: 
					key = labInfo[tdIndex]
					if key.lower() == 'actions':
						actions = []
						self.edit_button = row.find_element_by_class_name('edit-treatment-icon')
						self.delete_button = row.find_element_by_class_name('delete-treatment-icon')
						actions.append(self.edit_button)
						actions.append(self.delete_button)
						labResult[key] = actions
					else:
						text = td.text
						labResult[key] = text
			
			self.fish_tests.append(labResult)



	def load_gep_table(self):
		self.gep_tests = []
		gepTable = self.driver.find_element_by_id('gep_table')
		rows = gepTable.find_elements_by_class_name('table_row')
		labInfo = [] # add text from each header row to values list
		for rowIndex, row in enumerate(rows):
			labResult = {}
			divs = row.find_elements_by_tag_name('div')
			tds = row.find_elements_by_tag_name('td')
			# for divIndex, div in enumerate(divs):
			for tdIndex, td in enumerate(tds):
				if rowIndex == 0:
					labInfo.append(td.text.lower())
				else: 
					key = labInfo[tdIndex]
					if key.lower() == 'actions':
						actions = []
						self.edit_button = row.find_element_by_class_name('edit-treatment-icon')
						self.delete_button = row.find_element_by_class_name('delete-treatment-icon')
						actions.append(self.edit_button)
						actions.append(self.delete_button)
						labResult[key] = actions
					else:
						text = td.text
						labResult[key] = text
			
			self.gep_tests.append(labResult)

	def load_ngs_table(self):
		self.ngs_tests = []
		ngsTable = self.driver.find_element_by_id('ngs_table')
		rows = ngsTable.find_elements_by_class_name('table_row')
		labInfo = [] # add text from each header row to values list
		for rowIndex, row in enumerate(rows):
			labResult = {}
			tds = row.find_elements_by_tag_name('td')
			# for divIndex, div in enumerate(divs):
			for tdIndex, td in enumerate(tds):
				if rowIndex == 0:
					labInfo.append(td.text.lower())
				else: 
					key = labInfo[tdIndex]
					if key.lower() == 'actions':
						actions = []
						self.edit_button = row.find_element_by_class_name('edit-treatment-icon')
						self.delete_button = row.find_element_by_class_name('delete-treatment-icon')
						actions.append(self.edit_button)
						actions.append(self.delete_button)
						labResult[key] = actions
					else:
						text = td.text
						labResult[key] = text
			
			self.ngs_tests.append(labResult)

	def load_highRisk_table(self):
		highRiskTable = self.driver.find_element_by_id('yesno_table')
		rows = highRiskTable.find_elements_by_class_name('table_row')
		labInfo = []
		self.highRisk_tests = {}
		self.highRisk_tests['edit'] = highRiskTable.find_element_by_class_name('edit-treatment-icon')
		# {'High Beta-2 Microglobulin': 'Yes',
		# 	'High Lactate Dehydrogenase': 'I dont know',
		# 	'Low albumin': 'I dont know',
		# 	'edit': webElement,
		# }
		for i, row in enumerate(rows):
			if i > 0 and i < 4:
				tds = row.find_elements_by_tag_name('td')
				for tdIndex, td in enumerate(tds):
					if tdIndex == 0:
						name = td.text
					else:
						value = td.text
				self.highRisk_tests[name] = value

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
		test = self.get_test(testType, testIndex)

		if testType == 'fish':
			if action == 'edit':
				test['actions'][0].click()
			else:
				test['actions'][1].click()
				self.popUpForm = popUpForm.PopUpForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
				self.popUpForm.confirm(popUpAction)

		elif testType == 'gep':
			if action == 'edit':
				test['actions'][0].click()
			else:
				test['actions'][1].click()
				self.popUpForm = popUpForm.PopUpForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
				self.popUpForm.confirm(popUpAction)

		elif testType == 'ngs':
			if action == 'edit':	
				test['actions'][0].click()
			else:
				test['actions'][1].click()
				self.popUpForm = popUpForm.PopUpForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
				self.popUpForm.confirm(popUpAction)
		else:
			if action == 'edit':
				self.highRisk_tests['edit'].click()
				self.edit_high_risk(testValues, 'save')
			else:
				print('Error: Edit High Risk Test action not possible')


		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def edit_high_risk(self, riskInfo, action='save'):
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


	def get_test(self, testType, testIndex):
		if testType == 'fish':
			return self.fish_tests[testIndex]
		elif testType == 'gep':
			return self.gep_tests[testIndex]
		elif testType == 'ngs':
			return self.ngs_tests[testIndex]
		else:
			return self.highRisk_tests










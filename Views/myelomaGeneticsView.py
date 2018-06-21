from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import menu
from Components import header
from Components import fishTestForm
from Components import gepTestForm
from Components import ngsTestForm
from Components import editHighRiskForm
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

			self.edit_button = self.driver.find_element_by_class_name('editdetetegenetic')

			cont = self.driver.find_element_by_class_name('genetics-btn')
			self.continue_button = cont.find_element_by_tag_name('button')

			self.tables = self.driver.find_elements_by_class_name('marg-btm0')
			self.load_fish_table(self)





			# Load GEP table
			gepTable = tables[1]

			# Load NGS table
			ngsTable = tables[2]

			# Load


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
			# find divs in row
			# loop through divs
			if i == 0:
				# load text into values
				# append to values
			else:
				# load text into dictionary w/ corresponding 'value' as key
				# append to self.fish_tests

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

	def add_gep_test(self, gepInfo, action='save'):
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

	def edit_high_risk(self, riskInfo, action='save'):
		self.edit_button.click()
		self.editHighRiskForm = editHighRiskForm.EditHighRiskForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.editHighRiskForm.load())
		self.editHighRiskForm.submit(riskInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))











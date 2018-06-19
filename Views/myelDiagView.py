from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, TimeoutException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from viewExceptions import MsgError
from Components import myelomaDiagnosisFreshForm
from Components import myelomaDiagnosisSavedForm
from Components import menu
from Components import header
from Views import view

class MyelDiagView(view.View):
	postUrl = 'signup'

	def load(self, expectedState=None, expectedValues=None):
		try:
			self.view_state = self.get_view_state()
			if expectedState and expectedState != self.view_state:
				print('Myeloma Diagnosis: Expected state: "' + expectedState + '", got state: "' + self.view_state + '"')
			else:
				if self.view_state == 'fresh':
					self.myelomaDiagnosisFreshForm = myelomaDiagnosisFreshForm.MyelomaDiagnosisFreshForm(self.driver, expectedValues)
				else:
					self.myelomaDiagnosisSavedForm = myelomaDiagnosisSavedForm.MyelomaDiagnosisSavedForm(self.driver, expectedValues)
				self.menu = menu.Menu(self.driver)
				self.header = header.AuthHeader(self.driver)
				# self.validate()
				return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			pass
		return False

	# def validate(self):
	# 	failures = []
	# 	if self.createAccount_link.text != 'Create Account':
	# 		failures.append('1. Create Account link. Expecting text "Create Account", got "' + self.createAccount_link.text + '"')
	# 	if len(failures) > 0:
	# 		print(failures)
	# 		raise NoSuchElementException('Failed to load myelomaDiagnosisView')

	def get_view_state(self):
		# Is myelomaDiagnosisForm fresh or already saved?
		try:
			el = self.driver.find_element_by_id('newly_diagnosedYes')
			return 'fresh'
		except NoSuchElementException:
			return 'saved'

	# def createErrorObj(self, errorText):
	# 	errorType = 'undefined';
	# 	errorMsg = '';

	# 	if 'confirm your email address' in errorText:
	# 		errorType = 'confirmation'
	# 		errorMsg = 'homeView.login: Confirmation error'
	# 	elif 'invalid username or password' in errorText:
	# 		errorType = 'invalid credentials'
	# 		errorMsg = 'homeView.login: Invalid Credentials error'

	# 	return {
	# 		'errorText': errorText,
	# 		'errorType': errorType,
	# 		'errorMsg': errorMsg,
	# 	}

	def submitFreshForm(self, formInfo, expectedErrorType=None):
		try:
			if self.myelomaDiagnosisFreshForm.submit(formInfo):
				# Should be displaying 'saved' form
				try:
					WDW(self.driver, 10).until(lambda x: self.load('saved', formInfo))
					return True
				except TimeoutException:
					# Could not load view in 'saved' state
					self.error = self.readErrors()
					if self.error:
						raise MsgError('MyelomaDiagnosisFreshForm submit error')
		except MsgError:
			# Is form submission expected to fail?
			errorType = self.error['errorType']
			if expectedErrorType and errorType == expectedErrorType:
				return True
			print(self.error['errorMsg'])
			if errorType == 'undefined':
				print('Undefined error: ' + self.error['errorText'])
		return False

########################### Saved Form ##############################

	def add_physician(self, physicianInfo, expectedInfo=None, action='submit',):
		# Enter info and submit addPhysicianForm. Then reload page
		if self.myelomaDiagnosisSavedForm:
			if self.myelomaDiagnosisSavedForm.add_physician(physicianInfo, action):
				WDW(self.driver, 10).until(lambda x: self.load('saved', expectedInfo))
		elif self.myelomaDiagnosisFreshForm:
			# todo: handle working on fresh form
			pass

	def add_diagnosis(self, diagnosisInfo, expectedInfo=None, action='submit'):
		# Enter info and submit additionalDiagnosisForm. Then reload page
		if self.myelomaDiagnosisSavedForm:
			if self.myelomaDiagnosisSavedForm.add_diagnosis(diagnosisInfo, action):
				WDW(self.driver, 10).until(lambda x: self.load('saved', expectedInfo))
		elif self.myelomaDiagnosisFreshForm:
			# todo: handle working on fresh form
			pass

	def delete(self, del_type='diagnosis', index=0, expectedInfo=None, action='submit'):
		# Handles deleting physician or diagnosis
		if self.myelomaDiagnosisSavedForm:
			if self.myelomaDiagnosisSavedForm.delete(del_type, index, action):
				if del_type == 'diagnosis' and index == 0:
					WDW(self.driver, 10).until(lambda x: self.load('fresh', expectedInfo))
				else:
					WDW(self.driver, 10).until(lambda x: self.load('saved', expectedInfo))
		elif self.myelomaDiagnosisFreshForm:
			# todo: handle working on fresh form
			pass









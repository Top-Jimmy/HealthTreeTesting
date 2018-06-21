from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import addLabsForm
from Components import menu
from Components import header
from Views import view

class MyelomaLabsView(view.View):
	post_url = 'myeloma-labs'

	def load(self, formInfo=None):
		try:
			# Crap on left
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			self.form = self.driver.find_element_by_class_name('page-content-wrapper')
			buttons = self.form.find_element_by_tag_name('button')

			self.add_new_button = buttons[0]

			# self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def validate(self):
		failures = []
		if self.add_new_button.text != 'Add New Labs':
			failure.append('AddLabsView: Unexpected add new labs button text')
		# if self.createAccount_link.text != 'Create Account':
		# 	failures.append('1. Create Account link. Expecting text "Create Account", got "' + self.createAccount_link.text + '"')
		# if len(failures) > 0:
		# 	print(failures)
		# 	raise NoSuchElementException('Failed to load HomeView')

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

	# def submit(self, formInfo, expectedError=None, expectedWarnings=None):
	# 	try:
	# 		if self.aboutMeForm.enter_info(formInfo):
	# 			# Should be on myeloma diagnosis page
	# 			url = self.driver.current_url
	# 			if '/about-me' not in url:
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

	def add_new_lab(self, labInfo, action='save'):
		self.add_new_button.click()
		self.addLabsForm = addLabsForm.AddLabsForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.addLabsForm.load())
		self.addLabsForm.submit(labInfo, 'save')







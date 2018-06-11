from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import aboutMeForm
from Views import view

class AboutMeView(view.View):
	post_url = 'about-me'

	def load(self, formInfo=None):
		try:
			# Crap on left
			self.aboutMeForm = aboutMeForm.AboutMeForm(self.driver, formInfo)
			# self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def validate(self):
		failures = []
		if self.createAccount_link.text != 'Create Account':
			failures.append('1. Create Account link. Expecting text "Create Account", got "' + self.createAccount_link.text + '"')
		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load HomeView')

	def createErrorObj(self, errorText):
		errorType = 'undefined';
		errorMsg = '';

		if 'confirm your email address' in errorText:
			errorType = 'confirmation'
			errorMsg = 'homeView.login: Confirmation error'
		elif 'invalid username or password' in errorText:
			errorType = 'invalid credentials'
			errorMsg = 'homeView.login: Invalid Credentials error'

		return {
			'errorText': errorText,
			'errorType': errorType,
			'errorMsg': errorMsg,
		}

	def submit(self, formInfo, expectedError=None, expectedWarning=None):
		try:
			if self.aboutMeForm.enter_info(formInfo):
				# Should be on home page
				url = self.driver.current_url
				if '/about-me' not in url:
					self.error = self.readErrors()
					if self.error:
						raise MsgError('Login Error')
			return True
		except MsgError:
			# Is login expected to fail?
			errorType = self.error['errorType']
			if expectedError and errorType.lower() == expectedError.lower():
				return True
			print(self.error['errorMsg'])
			if errorType == 'undefined':
				print('Undefined error: ' + self.error['errorText'])
		except WarningError:
			# Is login expected to have warning?
			warningType = self.warning['type']
			if expectedWarning and warningType.lower() != expectedWarning.lower():
				print(self.warning['msg'])
				if warningType == 'undefined':
					print('Undefined warning: ' + self.warning['text'])
			else:
				return True
		return False

	def click_link(self, link):
		if link == 'create account':
			self.createAccount_link.click()
		elif link == 'forgot password':
			self.signInForm.forgotPassword_link.click()




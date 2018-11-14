from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import signInForm
from Views import view

class HomeView(view.View):
	post_url = ''

	def load(self):
		try:
			# Crap on left
			self.header = self.driver.find_element_by_tag_name('header')
			header_buttons = self.header.find_elements_by_tag_name('a')
			self.signInButton = header_buttons[0]
			self.createAccountButton = header_buttons[1]
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

	def login(self, credentials, expectedError=None, expectedWarning=None):
		try:
			self.signInButton.click()
			self.signInForm = signInForm.SignInForm(self.driver)
			if self.signInForm.enter_credentials(credentials):
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
		if link == 'terms of service':
			self.terms_of_service_link.click()
		elif link == 'privacy policy':
			self.privacy_policy_link.click()
		elif link == 'create account':
			self.createAccount_link.click()
		elif link == 'forgot password':
			self.signInForm.forgotPassword_link.click()





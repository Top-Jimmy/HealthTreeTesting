from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError
from Components import signInForm
from Components import createAcctForm
from Views import view

class CreateAcctView(view.View):
	postUrl = 'signup'

	def load(self):
		try:
			# Crap on left
			self.signInForm = signInForm.SignInForm(self.driver)
			self.createAccount_link = self.driver.find_elements_by_tag_name('a')[2]
			self.validate()
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

	def login(self, credentials, expectedErrorType=None):
		try:
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
			if expectedErrorType and errorType == expectedErrorType:
				return True
			print(self.error['errorMsg'])
			if errorType == 'undefined':
				print('Undefined error: ' + self.error['errorText'])
		return False

	def click_link(self, link):
		if link == 'create account':
			self.createAccount_link.click()
			self.createAcctForm = createAcctForm.CreateAcctForm(self.driver)
			return True

	def create_account(self, acctInfo, action):
		if acctInfo:
			self.createAcctForm.submit(acctInfo, action)
			return True
		return False






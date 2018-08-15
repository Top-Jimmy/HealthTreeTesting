from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import forgotPwForm
from Views import view
from utilityFuncs import UtilityFunctions

class ForgotPwView(view.View):
	post_url = 'forgot-password'

	def load(self):
		self.util = UtilityFunctions(self.driver)
		try:
			# Crap on left
			self.forgotPwForm = forgotPwForm.ForgotPwForm(self.driver)
			self.signIn_link = self.driver.find_elements_by_tag_name('a')[-1]
			self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def validate(self):
		failures = []
		if self.util.get_text(self.signIn_link) != 'sign in':
			failures.append('1. Sign In link. Expecting text "Sign In", got "' + self.util.get_text(self.signIn_link) + '"')
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
			'text': errorText,
			'type': errorType,
			'msg': errorMsg,
		}

	def reset_password(self, email, expectedErrorType=None, expectedWarning=None):
		try:
			if self.forgotPwForm.submit_form(email):
				# Should be on home page
				url = self.driver.current_url
				if '/about-me' not in url: # Didn't end up on right page
					self.error = self.readErrors()
					self.warning = self.forgotPwForm.read_warning()
					if self.error:
						raise MsgError('Login Error')
					elif self.warning:
						raise WarningError('Login Warning')
			return True
		except MsgError:
			# Is login expected to fail?
			errorType = self.error['type']
			if expectedErrorType and errorType.lower() != expectedErrorType.lower():
				print(self.error['msg'])
				if errorType == 'undefined':
					print('Undefined error: ' + self.error['text'])
			else:
				return True
		except WarningError:
			# Is pw reset form expected to have warning?
			warningType = self.warning['type']
			if expectedWarning and warningType.lower() != expectedWarning.lower():
				print(self.warning['msg'])
				if warningType == 'undefined':
					print('Undefined warning: ' + self.warning['text'])
			else:
				return True
		return False

	def click_link(self, link):
		if link == 'sign in':
			self.signIn_link.click()

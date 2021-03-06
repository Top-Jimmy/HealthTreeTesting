from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import aboutMeForm
from Components import feedbackForm
from Components import menu
from Components import header
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class AboutMeView(view.View):
	post_url = 'about-me'

	def load(self, formInfo=None):
		try:
			# Crap on left
			self.aboutMeForm = aboutMeForm.AboutMeForm(self.driver, formInfo)
			self.menu = menu.Menu(self.driver)
			
			self.header = header.AuthHeader(self.driver)
			# self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def submit(self, formInfo, expectedError=None, expectedWarnings=None):
		try:
			if self.aboutMeForm.enter_info(formInfo):
				# Should be on myeloma diagnosis page
				url = self.driver.current_url
				if '/about-me' not in url:
					self.error = self.readErrors()
					self.warnings = self.aboutMeForm.read_warnings()
					if self.error:
						raise MsgError('Login Error')
					elif self.warnings:
						raise WarningError('Submission warning')
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
		return False

	def feedback(self, feedbackText, action='cancel'):
		self.header.feedback_button.click()
		self.feedbackForm = feedbackForm.FeedbackForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.feedbackForm.load())
		self.feedbackForm.submit(feedbackText, action)



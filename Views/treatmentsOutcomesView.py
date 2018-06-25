from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import aboutMeForm
from Components import menu
from Components import header
from Views import view

class TreatmentsOutcomesView(view.View):
	post_url = 'about-me'

	def load(self, formInfo=None):
		try:
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			self.state = self.load_state()
			if self.state == 'fresh':
				# load new popup
				# todo: need new account to get this state
				pass

			# self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def load_state(self):
		# New user gets popup asking whether they have received treatments before (yes/no)
		#
		# class: custom1-add-treatment-btn (elliot's fresh form)
		try:
			self.add_treatments_button = self.driver.find_element_by_class_name('custom1-add-treatment-btn')
			return 'normal'
		except NoSuchElementException:
			self.add_treatments_button = None
			return 'fresh'

	def validate(self, expectedValues):
		failures = []

		if state == 'normal':
			if self.add_treatments_button and self.add_treatments_button.text != 'Add Treatments':
				failures.append('treatmentsOutcomesView: Unexpected text on add treatment button')
		else:
			# todo: Validate text on 'fresh' popup
			pass

		if len(failures) > 0:
			for failure in failures:
				print(failure)
				raise NoSuchElementException("Failed to load treatmentsOutcomesView")

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

	def add_treatment(self, treatmentInfo, expectedError=None, expectedWarnings=None):
		try:
			if self.state == 'normal':
				self.add_treatments_button.click()
				self.addTreatmentForm = addTreatmentForm.AddTreatmentForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.addTreatmentForm.load())
				if self.addTreatmentsForm.add_treatment(treatmentInfo):
					# what page? state?
					pass
			else:
				# todo: handle fresh popup
				pass
			# if self.aboutMeForm.enter_info(formInfo):
			# 	# Should be on myeloma diagnosis page
			# 	url = self.driver.current_url
			# 	if '/about-me' not in url:
			# 		self.error = self.readErrors()
			# 		self.warnings = self.aboutMeForm.read_warnings()
			# 		if self.error:
			# 			raise MsgError('Login Error')
			# 		elif self.warnings:
			# 			raise WarningError('Submission warning')
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

	# def click_link(self, link):
	# 	if link == 'create account':
	# 		self.createAccount_link.click()
	# 	elif link == 'forgot password':
	# 		self.signInForm.forgotPassword_link.click()




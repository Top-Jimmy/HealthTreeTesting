from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import menu
from Components import header
from Components import fishTestForm
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW


class MyelomaGeneticsView(view.View):
	post_url = 'myeloma-genetics'

	def load(self, formInfo=None):
		try:
			cont = self.driver.find_element_by_class_name('genetics-btn')
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			

			addDiagnosisButtons = self.driver.find_elements_by_class_name('addDiagnoisisButton')
			self.add_fish_button = addDiagnosisButtons[0]
			self.add_gep_button = addDiagnosisButtons[1]
			self.add_ngs_button = addDiagnosisButtons[2]

			self.continue_button = cont.find_element_by_tag_name('button')
			# self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

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










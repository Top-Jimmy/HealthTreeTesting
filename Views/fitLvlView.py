from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError
from Components import fitLvlForm
from Components import menu
from Components import header
from Views import view

class FitLvlView(view.View):
	postUrl = 'signup'

	def load(self):
		try:
			# Crap on left
			self.fitLvlForm = fitLvlForm.FitLvlForm(self.driver)
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			# self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False


	def submit(self, fitnessInfo, action='submit'):
		try:
			if self.fitLvlForm.submit(fitnessInfo, action):
				# Should be on fitness level
				url = self.driver.current_url
				if '/myeloma-genetics' not in url:
					self.error = self.readErrors()
					if self.error:
						raise MsgError('Form Submission Error')
				return True
		except MsgError:
			print('FitLvlView submit: Need to handle MsgError!')
		except WarningError:
			print('FitLvlView submit: Need to handle WarningError!')
		return False





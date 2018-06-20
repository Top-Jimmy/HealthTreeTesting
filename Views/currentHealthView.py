from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import currentHealthForm
from Components import menu
from Components import header
from Views import view

class CurrentHealthView(view.View):
	postUrl = 'signup'

	def load(self, expectedValues=None):
		try:
			# Crap on left
			self.currentHealthForm = currentHealthForm.CurrentHealthForm(self.driver, expectedValues)
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)

			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def submit(self, formInfo, action='submit'):
		try:
			if self.currentHealthForm.submit(formInfo, action):
				# Should be on fitness level
				url = self.driver.current_url
				if '/fitness-level' not in url:
					self.error = self.readErrors()
					if self.error:
						raise MsgError('Form Submission Error')
				return True
		except MsgError:
			print('CurrentHealthView submit: Need to handle MsgError!')
		except WarningError:
			print('CurrentHealthView submit: Need to handle WarningError!')
		return False
		# Not sure there is a valid circumstance for this form to fail



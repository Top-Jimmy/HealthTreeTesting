from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import menu
from Components import header
from Views import view

class TreatmentOptionsView(view.View):
	post_url = 'treatment-options'

	def load(self, formInfo=None):
		try:
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			self.tutorial_button = self.driver.find_element_by_class_name('videobtn')
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

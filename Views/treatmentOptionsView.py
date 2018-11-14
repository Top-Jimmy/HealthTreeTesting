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
			self.load_treatment_options()


			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def load_treatment_options(self):
		treatment_options = []
		self.form = self.driver.find_element_by_class_name('treatmenthr')
		treatment_buttons = self.form.find_elements_by_tag_name('button')
		for button in treatment_buttons:
			treatment_options.append(button)

		if len(treatment_options) < 1:
			raise NoSuchElementException('not loading treatment options')
			return False

		return True



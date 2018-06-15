import feedbackForm
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class AuthHeader():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		cont = self.driver.find_element_by_class_name('header-custom-col')
		buttons = cont.find_elements_by_tag_name('button')
		self.logout_button = buttons[0]
		self.feedback_button = buttons[1]
		self.validate()
		return True

	def validate(self):
		failures = []
		if self.logout_button.text != 'Logout':
			failures.append('AuthHeader: Unexpected logout button text: "' + self.logout_button.text + '"')
		if self.feedback_button.text != 'FEEDBACK':
			failures.append('AuthHeader: Unexpected feedback button text: "' + self.feedback_button.text + '"')

		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load header')

	def close_dialog(self):
		self.close_dialog_button.click()

	def sign_out(self):
		self.logout_button.click()

	def send_feedback(self, feedbackText, action='send'):
		self.feedback_button.click()
		self.feedbackForm = feedbackForm.FeedbackForm(self.driver)
		self.feedbackForm.submit(feedbackText, action)
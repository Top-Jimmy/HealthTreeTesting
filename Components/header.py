import feedbackForm


class AuthHeader():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		cont = self.driver.find_element_by_class_name('header-custom-col')
		buttons = cont.find_elements_by_tag_name('button')
		self.logout_button = buttons[0]
		self.feedback_button = buttons[1]
		return True

	def sign_out(self):
		self.logout_button.click()

	def send_feedback(self, feedback):
		self.feedback_button.click()
		self.feedbackForm = feedback.FeedbackForm(self.driver)
		self.feedbackForm.submit(feedback)
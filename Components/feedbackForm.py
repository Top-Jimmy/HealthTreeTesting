from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class FeedbackForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		time.sleep(.5)
		self.form = self.driver.find_element_by_class_name('editroll')
		buttons = self.form.find_elements_by_tag_name('button')

		self.close_button = buttons[0]

		self.feedback_input = self.form.find_element_by_tag_name('textarea')
		self.submit_button = buttons[1]
		self.cancel_button = buttons[2]
		return self.validate()
		

	def validate(self):
		failures = []
		if self.feedback_input.get_attribute('placeholder') != 'Your highly valuable feedback goes here...':
			failures.append('FeedbackForm: Unexpected textarea placeholder')
		if self.submit_button.text.lower() != 'submit':
			failures.append('FeedbackForm: Unexpected submit button text: "' + self.submit_button.text.lower() + '" does not equal submit')
		if self.cancel_button.text.lower() != 'cancel':
			failures.append('FeedbackForm: Unexpected cancel button text ' + self.cancel_button.text.lower())
		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load FeedbackForm')
			return False
		return True

	# def read_warning(self):
	# 	inputs = ['Sign In', 'Password']
	# 	warnings = []
	# 	for i, warning_el in enumerate([self.login_warning, self.password_warning]):
	# 		text = warning_el.text
	# 		if len(text) > 0:
	# 			warnings.append({
	# 				'inputName': inputs[i],
	# 				'text': text,
	# 			})
	# 	if len(warnings) > 0:
	# 		return warnings
	# 	return None

	# def interpret_warning(self, warningText):
	# 	warningType = 'undefined'
	# 	if warningText == 'Please enter a valid email address.':
	# 		warningType = 'invalid credentials'
	# 	elif warningText == 'Please enter username.':
	# 		warningType = 'missing username'
	# 	elif warningText == 'Please enter password.':
	# 		warningType = 'missing password'

	# 	return {
	# 		'msg': 'forgotPwForm: Submit form warning. ' + warningMsg,
	# 		'text': warningText,
	# 		'type': warningType,
	# 	}

	def submit(self, feedbackText, action='submit'):
		
		self.feedback_input.clear()
		self.feedback_input.send_keys(feedbackText)
		if action == 'submit':
			self.submit_button.click()
		else:
			self.cancel_button.click()
		return True


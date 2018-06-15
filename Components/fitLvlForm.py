import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class FitLvlForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_element_by_class_name('mui-form')
		self.rows = self.form.find_elements_by_class_name('fitness-form-group')

		self.questions = []
		for row in self.rows:
			labels = row.find_elements_by_tag_name('label')
			value = None
			for i, label in enumerate(labels):
				if i != 0:
					classes = label.get_attribute('class')
					if 'active' in classes:
						if i == 1:
							value = True
						elif i == 2:
							value = False
			self.questions.append(value)

		# self.validate()
		return True

	# def validate(self):
	# 	failures = []
	# 	if expectedValues:
	# 		if expectedValues['walk_sixhours'] == 'no' and not self.walk_sixhoursno_radio.get_attribute('checked'):
	# 			failure.append('FitLvlForm: Expecting "no" to walking six or more hours a week')
	# 		elif expectedValues['walk_sixhours'] == 'yes' and not self.walk_sixhoursyes_radio.get_attribute('checked'):
	# 			failure.append('FitLvlForm: Expecting "yes" to walking six or more hours a week')

	# 		if expectedValues['walk_fivehours'] == 'no' and not self.walk_fivehoursno_radio.get_attribute('checked'):
	# 			failure.append('FitLvlForm: Expecting "no" to walking five hours or less a week')
	# 		elif expectedValues['walk_fivehours'] == 'yes' and not self.walk_fivehoursyes_radio.get_attribute('checked'):
	# 			failure.append('FitLvlForm: Expecting "yes" to walking five hours or less a week')

	# 		if expectedValues['walk_unassisted'] == 'no' and not self.walk_unassistedno_radio.get_attribute('checked'):
	# 			failure.append('FitLvlForm: Expecting "no" to walking unassisted')
	# 		elif expectedValues['walk_unassisted'] == 'yes' and not self.walk_unassistedyes_radio.get_attribute('checked'):
	# 			failure.append('FitLvlForm: Expecting "yes" to walking unassisted')

	# 		if expectedValues['shop'] == 'no' and not self.walk_shopno_radio.get_attribute('checked'):
	# 			failure.append('FitLvlForm: Expecting "no" to shoppig unassisted')
	# 		elif expectedValues['shop'] == 'yes' and not self.walk_shopyes_radio.get_attribute('checked'):
	# 			failure.append('FitLvlForm: Expecting "yes" to shopping unassisted')

	# 	if len(failures) > 0:
	# 		print(failures)
	# 		raise NoSuchElementException('Failed to load CreateAcctForm')

	# def read_warning(self):
	# 	inputs = ['username', 'email', 'password', 'confirm password']
	# 	warnings = []
	# 	warning_els = [
	# 		self.username_warning, self.email_warning, self.password_warning, self.confirm_password_warning,
	# 	]
	# 	for i, warning_el in enumerate(warning_els):
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
	# 	warningMsg = ''
	# 	if warningText == 'Please enter a valid email address.':
	# 		warningType = 'Invalid credentials'
	# 		warningMsg = 'forgotPwForm: Submit form warning'

	# 	return {
	# 		'msg', warningMsg,
	# 		'text', warningText,
	# 		'type', warningType,
	# 	}

	def set_question(self, questionIndex, value):
		row = self.rows[questionIndex]

		labels = row.find_elements_by_tag_name('label')
		if value == True:
			labels[1].click()
		else:
			labels[2].click()

	def submit(self, fitnessInfo):
		for i, value in enumerate(fitnessInfo):
			self.set_question(i, value)
			time.sleep(.4)
			self.load()
			# if i <= len(self.questions):
			# 	self.set_question(i, value)
			# 	time.sleep(.4)
			# else:
			# 	self.load()

		return True

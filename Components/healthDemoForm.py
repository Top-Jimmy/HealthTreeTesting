import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class HealthDemoForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		anchors = self.form.find_elements_by_tag_name('a')
		small = self.form.find_elements_by_tag_name('small')
		# small[2] hidden element

		self.race_amer_radio = inputs[0]
		self.race_asian_radio = inputs[1]
		self.race_black_radio = inputs[2]
		self.race_native_radio = inputs[3]
		self.race_white_radio = inputs[4]

		self.ethn_hispanicyes_radio = inputs[5]
		self.ethn_hispanicno_radio = inputs[6]

		self.race_back_input = inputs[7]

		self.country_input = inputs[8]

		self.city_born_input = inputs[9]

		self.city_grow_input = inputs[10]

		self.city_adult_input = inputs[11]

		self.religion_input = inputs[12]

		self.marital_input = inputs[13]

		self.education_input = inputs[14]

		self.employment_input = inputs[15]

		self.health_insno_radio = inputs[16]
		self.health_insyes_radio = inputs[17]

		self.militaryno_radio = inputs[18]
		self.militaryyes_radio = inputs[19]



		self.validate()
		return True

	def validate(self):
		failures = []
		if expectedValues:
			if expectedValues['race'] == 'white' and not self.race_white_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expected "white" for race')
			elif expectedValues['race'] == 'American Indian' and not self.race_amer_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expected "American Indian for race')
			elif expectedValues['race'] == 'asian' and not self.race_asian_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expected "asian" for race')
			elif expectedValues['race'] == 'black' and not self.race_black_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expected "black" for race')
			elif expectedValues['race'] == 'native' and not self.race_native_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expected "native" for race')

			if expectedValues['ethnicity'] == 'not Hispanic' and not self.ethn_hispanicno_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expected "not Hispanic" for ethnicity')
			elif expectedValues['ethnicity'] == 'Hispanic' and not self.ethn_hispanicyes_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expected "Hispanic for ethnicity')

			if self.city_born_input.get_attribute('value') != expectedValues['city_born']:
				failure.append('HealthDemoForm: Expecting city where born "' + expectedValues['city_born'] + '", got "' + self.city_born_input.get_attribute('value') + '"')

			if self.city_grow_input.get_attribute('value') != expectedValues['city_grow']:
				failure.append('HealthDemoForm: Expecting city where grew up "' + expectedValues['city_grow'] + '", got "' + self.city_grow_input.get_attribute('value') + '"')

			if self.city_adult_input.get_attribute('value') != expectedValues['city_adult']:
				failure.append('HealthDemoForm: Expecting city where you live "' + expectedValues['city_adult'] + '", got "' + self.city_adult_input.get_attribute('value') + '"')

			if expectedValues['health_ins'] == 'no' and not self.health_insno_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expecting "no" to having healht insurance')
			elif expectedValues['health_ins'] == 'yes' and not self.health_insyes_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expecting "yes" to having health insurance')

			if expectedValues['military'] == 'no' and not self.militaryno_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expecting "no" to having served in the military')
			elif expectedValues['military'] == 'yes' and not self.militaryyes_radio.get_attribute('checked'):
				failure.append('HealthDemoForm: Expecting "yes" to having served in the military')

		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load CreateAcctForm')

	def read_warning(self):
		inputs = ['username', 'email', 'password', 'confirm password']
		warnings = []
		warning_els = [
			self.username_warning, self.email_warning, self.password_warning, self.confirm_password_warning,
		]
		for i, warning_el in enumerate(warning_els):
			text = warning_el.text
			if len(text) > 0:
				warnings.append({
					'inputName': inputs[i],
					'text': text,
				})
		if len(warnings) > 0:
			return warnings
		return None

	def interpret_warning(self, warningText):
		warningType = 'undefined'
		warningMsg = ''
		if warningText == 'Please enter a valid email address.':
			warningType = 'Invalid credentials'
			warningMsg = 'forgotPwForm: Submit form warning'

		return {
			'msg', warningMsg,
			'text', warningText,
			'type', warningType,
		}


	def enter_credentials(self, credentials):
		if credentials['username'] and credentials['password']:
			self.login_input.send_keys(credentials['username'])
			time.sleep(.4)
			self.password_input.send_keys(credentials['password'])
			time.sleep(.4)
			self.signIn_button.click()
			time.sleep(.4)
			return True
		return False
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class CreateAcctForm():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		anchors = self.form.find_elements_by_tag_name('a')
		small = self.form.find_elements_by_tag_name('small')
		# small[2] hidden element

		self.newlyDiagnosedno_radio = self.form.find_element_by_id('newly_diagnosedNo')
		self.newlyDiagnosedyes_radio = self.form.find_element_by_id('newly_diagnosedYes')

		self.dateDiagnosis_form-control = self.form.find_element_by_tag_name('form-control')

		self.whatDiagnosis_input = inputs[2]

		self.highRisk1_input = self.form.find_element_by_tag_name('highRisk1')
		self.highRisk2_input = self.form.find_element_by_id('highRisk2')
		self.highRisk3_input = self.form.find_element_by_id('highRisk3')

		self.stemCell1_input = self.form.find_element_by_id('stemCell1')
		self.stemCell2_input = self.form.find_element_by_id('stemCell2')
		self.stemCell3_input = self.form.find_element_by_id('stemCell3')

		self.boneLesion0_input = self.form.find_element_by_id('0')
		self.boneLesion1_input = self.form.find_element_by_id('1')
		self.boneLesion2_input = self.form.find_element_by_id('2')
		self.boneLesion3_input = self.form.find_element_by_id('3')

		self.facility_input = inputs[13]
		self.city_input = self.form.find_element_by_id('Last')
		self.state_input = inputs[15]

		self.add_diagno_input = self.form.find_element_by_id('yesno0')
		self.add_diagyes_input = self.form.find_element_by_id('yesno1')

		self.phys_name_input = self.form.find_element_by_id('physician_name_0')
		self.phys_facility_input = self.form.find_element_by_id('facility_name')
		self.phys_city_input = self.form.find_element_by_id('city')
		self.phys_state_input = inputs[21]

		# self.validate()
		return True

	def validate(self):
		failures = []
		if expectedValues['newly_diagnosed'] == 'no' and not self.newly_diagnosedNo.get_attribute('checked')
			failure.append('MyelDiagForm: Expecting "no" to being newly diagnosed')
		elif expectedValues['newly_diagnosed'] == 'yes' and not self.newly_diagnosedYes.get_attribute('checked')
			failure.append('MyelDiagForm: Expecting "yes" to being newly diagnosed')

		if self.dateDiagnosis_form-control.get_attribute('value') != expectedValues['date']:
				failures.append('MyelDiagForm: Expecting date of diagnosis "' + expectedValues['date'] + '", got "' + self.dateDiagnosis_form-control.get_attribute('value') + '"')

		if expectedValues['high_risk'] == 'no' and not self.highRisk1




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
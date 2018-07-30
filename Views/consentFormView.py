from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
from Components import popUpForm
from Components import menu
from Components import header
from Components import singleDatePicker
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class ConsentFormView(view.View):
	post_url = 'consent-form'

	def load(self, expectedInfo=None):
		try:
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)

			self.form = self.driver.find_elements_by_tag_name('form')[1]
			try:
				self.facility_name = self.form.find_elements_by_class_name('font-weight-bold')[1].text
			except NoSuchElementException:
				# Facility name is not required field on previous page (for now)
				self.facility_name = None

			self.load_preferences()
			self.other_input = self.form.find_element_by_id('other_value')

			# Patient Info
			self.first_name = self.form.find_element_by_id('patient_firstName')
			self.last_name = self.form.find_element_by_id('patient_lastName')
			self.rep_first_name = self.form.find_element_by_id('representative_firstName')
			self.rep_last_name = self.form.find_element_by_id('representative_lastName')
			self.date_input = self.form.find_element_by_class_name('date_picker_component')

			# Portal Info
			self.username = self.form.find_element_by_id('portal_username')
			self.password = self.form.find_element_by_id('portal_password')
			self.url = self.form.find_element_by_id('portal_url')

			# Order is not same as displayed on page (float right)
			self.buttons = self.form.find_elements_by_class_name('green-hvr-bounce-to-top')
			self.agree_button = self.buttons[0]
			self.do_not_agree_button = self.buttons[1]
			self.print_button = self.buttons[2]
			self.back_button = self.buttons[3]

			return self.validate(expectedInfo)
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def validate(self, expectedInfo):
		failures = []
		if len(self.buttons) != 4:
			failure.append('ConsentForm: Unexpected number of form buttons. Loaded ' + str(len(self.buttons)))
		if len(self.preference_inputs) != 12:
			failure.append('ConsentForm: Unexpected number of preference inputs. Loaded ' + str(len(self.preference_inputs)))

		if expectedInfo:
			# Validate facilities
			pass

		if len(failures) > 0:
			for failure in failures:
				print(failure)
				return False
		return True

	def load_preferences(self):
		self.preference_inputs = self.form.find_elements_by_class_name('checkbox-custom')
		self.preferences = {}

		for inputEl in self.preference_inputs:
			inputId = inputEl.get_attribute('id')
			self.preferences[inputId] = inputEl
		# 'access_all_records'
		# 'lab_reports'
		# 'history'
		# 'admission'
		# 'medication'
		# 'xray'
		# 'paperwork'
		# 'consult'
		# 'mental'
		# 'alcohol'
		# 'hiv'
		# 'other'

	def set_preferences(self, info, other_comment=None):
		for key in info:
			if key in self.preferences and not self.preferences[key].is_selected():
				self.preferences[key].click()

		if other_comment:
			self.other_input.clear()
			self.other_input.send_keys(other_comment)

	def get_preferences(self):
		selected_preferences = []
		for inputEl in self.preference_inputs:
			if inputEl.is_selected():
				selected_preferences.append(inputEl.get_attribute('id'))
		return selected_preferences

	def set_patient_info(self, info, dateType='typed'):
		# Patient
		if 'first name' in info:
			self.first_name.clear()
			self.first_name.send_keys(info['first name'])
		if 'last name' in info:
			self.last_name.clear()
			self.last_name.send_keys(info['last name'])

		# Representative (optional)
		if 'rep first name' in info:
			self.rep_first_name.clear()
			self.rep_first_name.send_keys(info['rep first name'])
		if 'rep last name' in info:
			self.rep_last_name.clear()
			self.rep_last_name.send_keys(info['rep last name'])

		# Date
		if 'date' in info:
			if dateType == 'typed':
				self.date_input.clear()
				self.date_input.send_keys(info['date'])
			elif dateType == 'picker':
				self.date_input.click()
				picker = singleDatePicker.SingleDatePicker(self.driver)
				picker.set_date(info['date'])

	def get_patient_info(self):
		patient_info = {}
		patient_info['first name'] = self.first_name.get_attribute('value')
		patient_info['last name'] = self.last_name.get_attribute('value')
		patient_info['rep first name'] = self.rep_first_name.get_attribute('value')
		patient_info['rep last name'] = self.rep_last_name.get_attribute('value')
		patient_info['date'] = self.date_input.get_attribute('value')
		return patient_info

	def set_portal_info(self, info):
		if info.get('username', None):
			self.username.clear()
			self.username.send_keys(info['username'])

		if info.get('password', None):
			self.password.clear()
			self.password.send_keys(info['password'])

		if info.get('url', None):
			self.url.clear()
			self.url.send_keys(info['url'])

	def get_portal_info(self):
		portal_info = {}
		portal_info['username'] = self.username.get_attribute('value')
		portal_info['password'] = self.password.get_attribute('value')
		portal_info['url'] = self.url.get_attribute('value')
		return portal_info

	def action(self, action='submit'):
		if action == 'submit':
			self.agree_button.click()
		elif action == 'back':
			self.back_button.click()







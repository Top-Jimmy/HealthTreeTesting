from Components import popUpForm
from Components import menu
from Components import header
from Components import singleDatePicker
from Views import view
from utilityFuncs import UtilityFunctions

from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class ConsentFormView(view.View):
	post_url = 'consent-form'

	def load(self, expectedInfo=None, editMode=False):
		try:
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			self.util = UtilityFunctions(self.driver)
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			print('0')

			# Verify consent form is in expected mode (normal or edit)
			if self.edit_mode() != editMode:
				print('ConsentForm: Incorrect mode. Expected editMode ' + str(editMode))
				return False

			self.form = self.driver.find_elements_by_tag_name('form')[1]
			print('1')
			try:
				self.facility_name = self.form.find_elements_by_class_name('font-weight-bold')[1].text
			except NoSuchElementException:
				# Facility name is not required field on previous page (for now)
				self.facility_name = None
			print('2')
			self.load_preferences()
			print('3')
			self.other_input = self.form.find_element_by_id('other_value')
			print('4')

			# Patient Info
			self.first_name = self.form.find_element_by_id('patient_firstName')
			self.last_name = self.form.find_element_by_id('patient_lastName')
			self.rep_first_name = self.form.find_element_by_id('representative_firstName')
			self.rep_last_name = self.form.find_element_by_id('representative_lastName')
			self.date_input = self.form.find_element_by_id('dateField')
			print('5')

			# Portal Info
			self.load_portal_login_info(editMode)
			print('6')

			# Order is not same as displayed on page (float right)
			self.buttons = self.form.find_elements_by_class_name('green-hvr-bounce-to-top')
			self.agree_button = self.buttons[0]
			self.do_not_agree_button = self.buttons[1]
			self.print_button = self.buttons[2]
			self.back_button = self.buttons[3]
			print('7')

			return self.validate(expectedInfo)
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def edit_mode(self):
		# Is consent form in edit mode?
		try:
			# Look for edit button for Portal Login Information
			el = self.driver.find_element_by_class_name('info-edit')
			return True
		except NoSuchElementException:
			return False

	def load_portal_login_info(self, editMode):
		self.edit_login_info_button = self.try_load_edit_login_info_button()

		if editMode and self.login_info_mode() == 'noneditable':
			# No inputs. Load text as values
			vals = self.driver.find_elements_by_class_name('account-val')
			self.username = self.util.get_text(vals[0])
			self.password = self.util.get_text(vals[1])
			self.url = self.util.get_text(vals[2])
		else:
			# Editable. Load input elements
			self.username = self.form.find_element_by_id('portal_username')
			self.password = self.form.find_element_by_id('portal_password')
			self.url = self.form.find_element_by_id('portal_url')

	def try_load_edit_login_info_button(self):
		# Button for entering edit mode for 'Patient Portal Login Information'
		# Only exists when editing consent form
		try:
			return self.driver.find_element_by_class_name('info-edit')
		except NoSuchElementException:
			return None

	def login_info_mode(self):
		# Is login information editable?
		try:
			# Look for non-editable fields
			els = self.driver.find_elements_by_class_name('account-val')
			if len(els) == 3:
				return 'noneditable'
		except NoSuchElementException:
			return 'editable'

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
		for key in self.preferences:
			if key in info:
				# Make sure it's selected
			 	if not self.preferences[key].is_selected():
					self.util.click_el(self.preferences[key])
			else:
				# Make sure it's de-selected
				if self.preferences[key].is_selected():
					self.util.click_el(self.preferences[key])

		if other_comment:
			self.util.set_input(self.other_input, other_comment)

	def get_preferences(self):
		selected_preferences = []
		for inputEl in self.preference_inputs:
			if inputEl.is_selected():
				selected_preferences.append(inputEl.get_attribute('id'))
		return selected_preferences

	def set_patient_info(self, info, dateType='typed'):
		# Patient
		if 'first name' in info:
			self.util.set_input(self.first_name, info['first name'])
		if 'last name' in info:
			self.util.set_input(self.last_name, info['last name'])

		# Representative (optional)
		if 'rep first name' in info:
			self.util.set_input(self.rep_first_name, info['rep first name'])
		if 'rep last name' in info:
			self.util.set_input(self.rep_last_name, info['rep last name'])

		# Date
		if 'date' in info:
			if dateType == 'typed':
				self.util.set_input(self.date_input, info['date'])
			elif dateType == 'picker':
				self.util.click_el(self.date_input)
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
		if self.edit_mode() and self.login_info_mode() == 'uneditable':
			self.util.click_el(self.edit_login_info_button)
			time.sleep(.4)
			self.load()

		if info.get('username', None):
			self.util.set_input(self.username, info['username'])

		if info.get('password', None):
			self.util.set_input(self.password, info['password'])

		if info.get('url', None):
			self.util.set_input(self.url, info['url'])

	def get_portal_info(self):
		portal_info = {}
		editMode = self.edit_mode()
		portalInfoMode = self.login_info_mode()
		if editMode and portalInfoMode == 'noneditable':
			# Info is not editable. Password will be replaced w/ * characters
			portal_info['username'] = self.username
			portal_info['password'] = self.password
			portal_info['url'] = self.url
		else:
			portal_info['username'] = self.username.get_attribute('value')
			portal_info['password'] = self.password.get_attribute('value')
			portal_info['url'] = self.url.get_attribute('value')
		return portal_info

	def action(self, action='submit'):
		if action == 'submit':
			self.util.click_el(self.agree_button)
		elif action == 'back':
			self.util.click_el(self.back_button)
		elif action == 'do not agree':
			self.util.click_el(self.do_not_agree_button)







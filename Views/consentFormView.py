from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from Components import popUpForm
from Components import menu
from Components import header
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ConsentFormView(view.View):
	post_url = 'consent-form'

	def load(self, expectedInfo=None):
		try:
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)

			self.form = self.driver.find_elements_by_tag_name('form')[1]

			self.all_records = self.form.find_element_by_id('access_all_records')

			self.lab_results = self.form.find_element_by_id('lab_reports')
			self.history = self.form.find_element_by_id('history')
			self.admission = self.form.find_element_by_id('admission')
			self.medication = self.form.find_element_by_id('medication')
			self.xray = self.form.find_element_by_id('xray')
			self.paperwork = self.form.find_element_by_id('paperwork')
			self.consult = self.form.find_element_by_id('consult')
			self.mental = self.form.find_element_by_id('mental')
			self.alcohol = self.form.find_element_by_id('alcohol')
			self.hiv = self.form.find_element_by_id('hiv')
			self.other = self.form.find_element_by_id('other')
			self.other_input = self.form.find_element_by_id('other_value')

			# Patient Name
			self.first_name = self.form.find_element_by_id('patient_firstName')
			self.last_name = self.form.find_element_by_id('patient_lastName')

			# Patient Representative
			self.rep_first_name = self.form.find_element_by_id('')
			self.rep_last_name = self.form.find_element_by_id('')

			self.date_input = self.form.find_elements_by_class_name('date_picker_component')

			# Portal Info
			self.username = self.form.find_element_by_id('portal_username')
			self.password = self.form.find_element_by_id('portal_password')
			self.url = self.form_find_element_by_id('portal_url')


			# Order is not same as displayed on page (float right)
			self.buttons = self.container.find_elements_by_class_name('green-hvr-bounce-to-top')
			self.agree_button = buttons[0]
			self.do_not_agree_button = buttons[1]
			self.print_button = buttons[2]
			self.back_button = buttons[3]

			return self.validate(expectedInfo)
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def validate(self, expectedInfo):
		failures = []
		if len(self.buttons) != 4:
			failure.append('ConsentForm: Unexpected number of form buttons. Expected 4, loaded ' + str(len(self.buttons)))

		if expectedInfo:
			# Validate facilities
			pass

		if len(failures) > 0:
			for failure in failures:
				print(failure)
				return False
		return True



from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import addLabsForm
from Components import popUpForm
from Components import menu
from Components import header
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class MyelomaLabsView(view.View):
	post_url = 'myeloma-labs'

	def load(self, formInfo=None):
		try:
			# Crap on left
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			self.form = self.driver.find_element_by_id('page-content-wrapper')
			buttons = self.form.find_elements_by_tag_name('button')
			inputs = self.form.find_elements_by_tag_name('input')

			self.add_new_button = buttons[0]
			self.lab_values_dropdown = buttons[1]
			self.three_month_button = buttons[2]
			self.six_month_button = buttons[3]
			self.year_to_date_button = buttons[4]
			self.one_year_button = buttons[5]
			self.two_year_button = buttons[6]
			self.five_year_button = buttons[7]
			self.ten_year_button = buttons[8]
			self.all_button = buttons[9]

			self.continue_button = buttons[10]

			self.from_date_input = inputs[0]

			self.to_date_input = inputs[1]

			self.load_table()
			print(self.clinical_tables	)

			self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def validate(self):
		failures = []
		if self.add_new_button.text != 'Add New Labs':
			failure.append('AddLabsView: Unexpected add new labs button text')


	def load_table(self):
		self.clinical_tables = []
		clinical_table = self.form.find_element_by_id('clinical_table')
		rows = clinical_table.find_elements_by_class_name('table_row')
		keys = ['actions', 'dobd', 'monoclonal', 'kappa', 'lambda', 'ratio', 'bone_marrow', 'blood', 'blood_cell', 'hemoglobin',  'lactate', 'albumin', 'immuno_g', 'immuno_a', 'immuno_m', 'calcium', 'platelets']
		for rowIndex, row in enumerate(rows):
			rowInfo = {} # Info for an individual test
			if rowIndex != 0:
				tds = row.find_elements_by_tag_name('td')
				for tdIndex, td in enumerate(tds):
					if tdIndex == 0:
						buttons = row.find_elements_by_tag_name('i')
						rowInfo['edit'] = row.find_element_by_class_name('edit')
						rowInfo['delete'] = row.find_element_by_class_name('delete')
					else:
						rowInfo[keys[tdIndex]] = td.text.lower()
			if rowInfo:
				self.clinical_tables.append(rowInfo)

	# def validate_table(self):
		

	def get_my_labs(self):
		self.add_new_button.click()
		self.addLabsForm = addLabsForm.AddLabsForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.addLabsForm.load())
		self.addLabsForm.get_my_labs_button.click() # Should now be on /my-labs-facilities

	def add_new_lab(self, labInfo, action='save'):
		self.add_new_button.click()
		self.addLabsForm = addLabsForm.AddLabsForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.addLabsForm.load())
		self.addLabsForm.submit(labInfo, 'save')
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def edit_delete_lab(self, testIndex, revisedLabInfo, action='delete', popUpAction='confirm'):
		try:
			test = self.clinical_tables[testIndex]
		except IndexError:
			print('No test w/ index: ' + str(testIndex))
			return False

		if test:
			if action == 'delete':
				test['delete'].click()
				self.popUpForm = popUpForm.PopUpForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.popUpForm.load())
				self.popUpForm.confirm(popUpAction)
			else:
				test['edit'].click()
				WDW(self.driver, 10).until(lambda x: self.addLabsForm.load())
				self.addLabsForm.submit(revisedLabInfo, 'save')

			return True





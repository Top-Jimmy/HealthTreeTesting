from viewExceptions import MsgError, WarningError
from Components import addLabsForm
from Components import popUpForm
from Components import menu
from Components import header
from Views import view
from utilityFuncs import UtilityFunctions

from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class MyelomaLabsView(view.View):
	post_url = 'myeloma-labs'

	def load(self, labInfo=None):
		try:
			# Crap on left
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

			self.util = UtilityFunctions(self.driver)
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

			# self.load_table()
			# self.validate(labInfo)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def validate(self, labInfo):
		failures = []
		loadedInfo = self.clinical_tables[-1]
		if loadedInfo:
			if labInfo:
				if loadedInfo['dobd'] != labInfo['dobd']:
					failures.append('Table value: ' + '"' + str(loadedInfo['dobd']) + '"' + ' expected ' + '"' + str(labInfo['dobd']) + '"')
				if loadedInfo['monoclonal'] != labInfo['monoclonal']:
					failures.append('Table value: ' + '"' + str(loadedInfo['monoclonal']) + '"' + ' expected ' + '"' + str(labInfo['monoclonal']) + '"')
				if loadedInfo['kappa'] != labInfo['kappa']:
					failures.append('Table value: ' + '"' + str(loadedInfo['kappa']) + '"' + ' expected ' + '"' + str(labInfo['kappa']) + '"')
				if loadedInfo['lambda'] != labInfo['lambda']:
					failures.append('Table value: ' + '"' + str(loadedInfo['lambda']) + '"' + ' expected ' + '"' + str(labInfo['lambda']) + '"')
				if loadedInfo['ratio'] != labInfo['ratio']:
					failures.append('Table value: ' + '"' + str(loadedInfo['ratio']) + '"' + ' expected ' + '"' + str(labInfo['ratio']) + '"')
				if loadedInfo['bone_marrow'] != labInfo['bone_marrow']:
					failures.append('Table value: ' + '"' + str(loadedInfo['bone_marrow']) + '"' + ' expected ' + '"' + str(labInfo['bone_marrow']) + '"')
				if loadedInfo['blood'] != labInfo['blood']:
					failures.append('Table value: ' + '"' + str(loadedInfo['blood']) + '"' + ' expected ' + '"' + str(labInfo['blood']) + '"')
				if loadedInfo['blood_cell'] != labInfo['blood_cell']:
					failures.append('Table value: ' + '"' + str(loadedInfo['blood_cell']) + '"' + ' expected ' + '"' + str(labInfo['blood_cell']) + '"')
				if loadedInfo['hemoglobin'] != labInfo['hemoglobin']:
					failures.append('Table value: ' + '"' + str(loadedInfo['hemoglobin']) + '"' + ' expected ' + '"' + str(labInfo['hemoglobin']) + '"')
				if loadedInfo['lactate'] != labInfo['lactate']:
					failures.append('Table value: ' + '"' + str(loadedInfo['lactate']) + '"' + ' expected ' + '"' + str(labInfo['lactate']) + '"')
				if loadedInfo['albumin'] != labInfo['albumin']:
					failures.append('Table value: ' + '"' + str(loadedInfo['albumin']) + '"' + ' expected ' + '"' + str(labInfo['albumin']) + '"')
				if loadedInfo['immuno_g'] != labInfo['immuno_g']:
					failures.append('Table value: ' + '"' + str(loadedInfo['immuno_g']) + '"' + ' expected ' + '"' + str(labInfo['immuno_g']) + '"')
				if loadedInfo['immuno_a'] != labInfo['immuno_a']:
					failures.append('Table value: ' + '"' + str(loadedInfo['immuno_a']) + '"' + ' expected ' + '"' + str(labInfo['immuno_a']) + '"')
				if loadedInfo['immuno_m'] != labInfo['immuno_m']:
					failures.append('Table value: ' + '"' + str(loadedInfo['immuno_m']) + '"' + ' expected ' + '"' + str(labInfo['immuno_m']) + '"')
				if loadedInfo['calcium'] != labInfo['calcium']:
					failures.append('Table value: ' + '"' + str(loadedInfo['calcium']) + '"' + ' expected ' + '"' + str(labInfo['calcium']) + '"')
				if loadedInfo['platelets'] != labInfo['platelets']:
					failures.append('Table value: ' + '"' + str(loadedInfo['platelets']) + '"' + ' expected ' + '"' + str(labInfo['platelets']) + '"')
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


	def get_my_labs(self):
		self.add_new_button.click()
		self.addLabsForm = addLabsForm.AddLabsForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.addLabsForm.load())
		self.util.click_el(self.addLabsForm.get_my_labs_button) # Should now be on /my-labs-facilities

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





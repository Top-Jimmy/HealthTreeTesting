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
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			self.util = UtilityFunctions(self.driver)
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)
			self.form = self.driver.find_element_by_id('page-content-wrapper')
			buttons = self.form.find_elements_by_tag_name('button')
			inputs = self.form.find_elements_by_tag_name('input')

			self.add_new_labs = buttons[0]
			self.get_my_labs = buttons[1] # Is this here all the time?

			# Lab Values Chart
			chart_cont = self.driver.find_element_by_class_name('myeloma-labs-custom')
			self.lab_values_dropdown = chart_cont.find_element_by_tag_name('button')

			# Date range options
			range_cont = self.driver.find_element_by_class_name('datenfilter')
			date_buttons = range_cont.find_elements_by_tag_name('button')
			self.three_month_button = date_buttons[0]
			self.six_month_button = date_buttons[1]
			self.year_to_date_button = date_buttons[2]
			self.one_year_button = date_buttons[3]
			self.two_year_button = date_buttons[4]
			self.five_year_button = date_buttons[5]
			self.ten_year_button = date_buttons[6]
			self.all_button = date_buttons[7]

			# Custom date range
			inputs = range_cont.find_elements_by_tag_name('input')
			self.from_date_input = inputs[0]
			self.to_date_input = inputs[1]

			# Lab Values Table
			self.load_table()

			self.continue_button = buttons[10]


			# self.validate(labInfo)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def validate(self, labInfo):
		failures = []
		lInfo = self.clinical_tables[-1]
		if lInfo:
			if labInfo:
				if lInfo['dobd'] != labInfo['dobd']:
					failures.append('Table value: ' + '"' + str(lInfo['dobd']) + '"' + ' expected ' + '"' + str(labInfo['dobd']) + '"')
				
				# 1: Clinical Trials
				if lInfo['monoclonal'] != labInfo['monoclonal']:
					failures.append('Table value: ' + '"' + str(lInfo['monoclonal']) + '"' + ' expected ' + '"' + str(labInfo['monoclonal']) + '"')
				if lInfo['kappa'] != labInfo['kappa']:
					failures.append('Table value: ' + '"' + str(lInfo['kappa']) + '"' + ' expected ' + '"' + str(labInfo['kappa']) + '"')
				if lInfo['lambda'] != labInfo['lambda']:
					failures.append('Table value: ' + '"' + str(lInfo['lambda']) + '"' + ' expected ' + '"' + str(labInfo['lambda']) + '"')
				if lInfo['ratio'] != labInfo['ratio']:
					failures.append('Table value: ' + '"' + str(lInfo['ratio']) + '"' + ' expected ' + '"' + str(labInfo['ratio']) + '"')
				if lInfo['bone_marrow'] != labInfo['bone_marrow']:
					failures.append('Table value: ' + '"' + str(lInfo['bone_marrow']) + '"' + ' expected ' + '"' + str(labInfo['bone_marrow']) + '"')

				if lInfo['creatinine'] != labInfo['creatinine']:
					failures.append('Table value: ' + '"' + str(lInfo['creatinine']) + '"' + ' expected ' + '"' + str(labInfo['creatinine']) + '"')
				if lInfo['platelets'] != labInfo['platelets']:
					failures.append('Table value: ' + '"' + str(lInfo['platelets']) + '"' + ' expected ' + '"' + str(labInfo['platelets']) + '"')
				if lInfo['neutrophils'] != labInfo['neutrophils']:
					failures.append('Table value: ' + '"' + str(lInfo['neutrophils']) + '"' + ' expected ' + '"' + str(labInfo['neutrophili']) + '"')
				
				# if lInfo['blood'] != labInfo['blood']:
				# 	failures.append('Table value: ' + '"' + str(lInfo['blood']) + '"' + ' expected ' + '"' + str(labInfo['blood']) + '"')
				
				# 2: Current state
				if lInfo['calcium'] != labInfo['calcium']:
					failures.append('Table value: ' + '"' + str(lInfo['calcium']) + '"' + ' expected ' + '"' + str(labInfo['calcium']) + '"')
				if lInfo['blood_cell'] != labInfo['blood_cell']:
					failures.append('Table value: ' + '"' + str(lInfo['blood_cell']) + '"' + ' expected ' + '"' + str(labInfo['blood_cell']) + '"')
				if lInfo['hemoglobin'] != labInfo['hemoglobin']:
					failures.append('Table value: ' + '"' + str(lInfo['hemoglobin']) + '"' + ' expected ' + '"' + str(labInfo['hemoglobin']) + '"')
				if lInfo['lactate'] != labInfo['lactate']:
					failures.append('Table value: ' + '"' + str(lInfo['lactate']) + '"' + ' expected ' + '"' + str(labInfo['lactate']) + '"')
				if lInfo['albumin'] != labInfo['albumin']:
					failures.append('Table value: ' + '"' + str(lInfo['albumin']) + '"' + ' expected ' + '"' + str(labInfo['albumin']) + '"')
				if lInfo['immuno_g'] != labInfo['immuno_g']:
					failures.append('Table value: ' + '"' + str(lInfo['immuno_g']) + '"' + ' expected ' + '"' + str(labInfo['immuno_g']) + '"')
				if lInfo['immuno_a'] != labInfo['immuno_a']:
					failures.append('Table value: ' + '"' + str(lInfo['immuno_a']) + '"' + ' expected ' + '"' + str(labInfo['immuno_a']) + '"')
				if lInfo['immuno_m'] != labInfo['immuno_m']:
					failures.append('Table value: ' + '"' + str(lInfo['immuno_m']) + '"' + ' expected ' + '"' + str(labInfo['immuno_m']) + '"')
				
				if lInfo['platelets'] != labInfo['platelets']:
					failures.append('Table value: ' + '"' + str(lInfo['platelets']) + '"' + ' expected ' + '"' + str(labInfo['platelets']) + '"')
		if self.add_new_labs.text != 'Add New Labs':
			failures.append('AddLabsView: Unexpected add new labs button text')

		if len(failures) > 0:
			for failure in failures:
				print(failure)
				return False
		return True


	def load_table(self):
		# Table with saved Lab results at bottom of page
		# Read info from each row and return dictionary
		self.clinical_tables = []

		# Table Header
		try:
			table_header = self.form.find_element_by_class_name('sticky-table-header-wrapper')
		except NoSuchElementException:
			# No lab results saved (or table not displayed yet)
			return None
		header_cells = table_header.find_elements_by_class_name('sticky-table-cell')
		header_keys = ['actions', 'dobd', 'monoclonal', 'kappa', 'lambda', 'ratio', 'bone_marrow', 'creatine', 'platelets', 'neutrophils', 'blood_cell', 'hemoglobin',  'lactate', 'albumin', 'immuno_g', 'immuno_a', 'immuno_m', 'calcium']

		# Table Body
		table_body = self.form.find_element_by_class_name('sticky-table-y-wrapper')
		# Actions, Lab date
		stationary_content = table_body.find_element_by_class_name('sticky-table-table')
		stationary_rows = stationary_content.find_elements_by_class_name('sticky-table-row')
		# self.clinical_tables.append({'delete': stationary_rows[0].find_element_by_class_name('delete')})
		# Lab fields
		sliding_content = table_body.find_element_by_class_name('sticky-table-x-wrapper')
		sliding_rows = sliding_content.find_elements_by_class_name('sticky-table-row')

		for rowIndex, row in enumerate(stationary_rows):
			# print(rowIndex)
			rowInfo = {} # Info for an individual lab result
			stationary_row = row
			rowInfo['edit'] = stationary_row.find_element_by_class_name('edit')
			rowInfo['delete'] = stationary_row.find_element_by_class_name('delete')
			rowInfo['date'] = stationary_row.find_elements_by_class_name('sticky-table-cell')[1].text

			sliding_row = sliding_rows[rowIndex]
			cells = sliding_row.find_elements_by_class_name('sticky-table-cell')
			if rowIndex < 5:
				print(len(cells))
			for cellIndex, cell in enumerate(cells):
				rowInfo[header_keys[cellIndex]] = cell.text.lower()
			if rowInfo:
				self.clinical_tables.append(rowInfo)


	def get_my_labs(self):
		self.add_new_labs.click()
		self.addLabsForm = addLabsForm.AddLabsForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.addLabsForm.load())
		self.util.click_el(self.addLabsForm.get_my_labs_button) # Should now be on /my-labs-facilities

	def add_new_lab(self, labInfo, action='save'):
		self.add_new_labs.click()
		self.addLabsForm = addLabsForm.AddLabsForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.addLabsForm.load())
		self.addLabsForm.submit(labInfo, 'save')
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def edit_delete_lab(self, testIndex=0, revisedLabInfo=None, action='delete', popUpAction='confirm'):
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

	def delete_all_labs(self):
		while self.clinical_tables:
			self.edit_delete_lab()
			time.sleep(2)
			self.load()




from selenium.common.exceptions import (NoSuchElementException,
	ElementNotVisibleException, StaleElementReferenceException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
import time

class DatePicker():
	"""Date picker for MonthYear input"""

	def __init__(self, driver):
		self.driver = driver

	def load(self, expectedState=None):
		try:
			self.picker_state = self.get_picker_state()
			if self.picker_state == 'undefined':
				print('DatePicker: undefined state')
				return False
			elif expectedState and expectedState != self.picker_state:
				print('DatePicker: Expected state: "' + expectedState + '". Got state: "' + self.picker_state + '"')
				return False
			else:
				time.sleep(.4)
				if self.picker_state == 'month':
					# Header should display current year. # Picker table should have months
					self.cont = self.driver.find_element_by_class_name('rdtMonths')
					self.tables = self.cont.find_elements_by_tag_name('table')

					self.picker_table = self.tables[1]
					self.months = self.load_picker_table_items('month')
				else: # Header should display range of years, picker table should display those years
					self.cont = self.driver.find_element_by_class_name('rdtYears')
					self.tables = self.cont.find_elements_by_tag_name('table')

					self.picker_table = self.tables[1]
					self.years = self.load_picker_table_items('year')

				header = self.tables[0]
				self.previous_button = header.find_element_by_class_name('rdtPrev')
				self.next_button = header.find_element_by_class_name('rdtNext')
				self.current_button = header.find_element_by_class_name('rdtSwitch')

				self.current_year = self.load_current_year()
				self.current_month = self.load_current_month()
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

	def get_picker_state(self):
		# Currently selecting years or months? Default should be months
		state = 'undefined'
		try:
			el = self.driver.find_element_by_class_name('rdtYears')
			state = 'year'
		except NoSuchElementException:
			pass

		if state == 'undefined':
			try:
				el = self.driver.find_element_by_class_name('rdtMonths')
				state = 'month'
			except NoSuchElementException:
				pass
		return state

	def load_picker_table_items(self, expectedType):
		# If state matches expectedType, return dict of tds in picker table
		if expectedType and expectedType == self.picker_state:
			items = {}
			if self.picker_table:
				tds = self.picker_table.find_elements_by_tag_name('td')
				for i, td in enumerate(tds):
					items[td.text] = tds[i]
				return items


########################### General ##############################

	def set_date(self, date):
		month = self.parse_date(date, 'month')
		year = self.parse_date(date, 'year')
		self.load()
		if self.current_year != year:
			self.set_year(year)
		if self.current_month != month:
			self.set_month(month)
		# Wait for datepicker to disappear
		time.sleep(.4)

		# try:
		# 	if self.current_year != year:
		# 		self.set_year(year)
		# 	if self.current_month != month:
		# 		self.set_month(month)
		# 	# Wait for datepicker to disappear
		# 	time.sleep(.4)
		# except (StaleElementReferenceException, ElementNotVisibleException, WebDriverException) as e:
		# 	# page probably reloaded.
		# 	dateElement.click()
		# 	self.load()
		# 	self.set_date(date)


	def parse_date(self, dateStr, dateType):
		# Given dateStr "mm/yyyy", parse and return month or year
		divider = dateStr.index('/')
		if dateType == 'month':
			months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
			return months[int(dateStr[:divider])]
		else:
			year = dateStr[divider + 1:]
			return year


########################### Month Picker ##############################

	def load_current_month(self):
		# Return first 3 letters of currently selected month (None if none selected or picking year)
		if self.picker_state == 'month':
			for month, element in self.months.iteritems():
				classes = element.get_attribute('class')
				if 'rdtActive' in classes:
					# if element.get_attribute('class').contains('rdtActive'):
					# .get_attribute(class) returns unicode object. Cannot call .contains() on unicode object
					return month
		return None

	def load_months(self):
		# Return dict of month elements. Key is first 3 letters of month.
		if self.picker_state == 'month':
			months = {}
			if self.picker_table:
				month_tds = self.picker_table.find_elements_by_tag_name('td')
				for i, month in enumerate(month_tds):
					months[month.text] = month_tds[i]
			return months

	def get_month_status(self, month):
		# Is given month enabled or disabled?
		if self.picker_state == 'month' and self.months:
			classes = self.months[month].get_attribute('class')
			if 'rdtDisabled' in classes:
				# if self.months[month].get_attribute('class').contains('rdtDisabled'):
				# .get_attribute(class) returns unicode object. Cannot call .contains() on unicode object
				return 'disabled'
			else:
				return 'enabled'

	def set_month(self, month):
		if self.picker_state == 'month':
			# Is month enabled?
			if self.get_month_status(month) == 'enabled':
				self.months[month].click()
				return True
		return False


########################### Year Picker ##############################

	def set_year(self, year):
		if self.picker_state == 'month':
			self.current_button.click()
			WDW(self.driver, 3).until(lambda x: self.load('year'))

		# Is year visible? Before or after current page?
		first_year = self.get_earliest_year()
		last_year = first_year + 11 	# Always displays 12 years
		if year < first_year:
			self.previous_button.click()
			self.load('year')
			self.set_year(year)
		elif year > last_year:
			self.next_button.click()
			self.load('year')
			self.set_year(year)
		else:
			self.years[year].click()
			self.load('month')

	def get_earliest_year(self):
		# Return earliest year visible on year picker
		if self.picker_state == 'year' and self.years:
			lowest_year = 3000
			for year, element in self.years.iteritems():
				if int(year) < lowest_year:
					lowest_year = int(year)
			if lowest_year < 3000:
				return lowest_year
			else:
				print('Datepicker: Failed to get earliest year')

	def load_current_year(self):
		if self.picker_state == 'month':
			return self.current_button.text



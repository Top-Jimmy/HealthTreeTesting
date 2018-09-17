from selenium.common.exceptions import (NoSuchElementException,
  ElementNotVisibleException, StaleElementReferenceException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
import time

from utilityFuncs import UtilityFunctions

# flatpickr component: Datepicker for selecting Day/Month/Year.
# Used on Consent Form
class SingleDatePicker():

  def __init__(self, driver):
    self.driver = driver
    self.util = UtilityFunctions(self.driver)

  def load(self, expectedState=None):
    # Should be 2 elements w/ this class. Grab 2nd
    time.sleep(3)
    raw_input('about to look for showTimeInput')
    containers = self.driver.find_elements_by_class_name('showTimeInput') 
    self.container = containers[-1]
    # self.container = self.driver.find_element_by_class_name('react-datepicker')

    el = self.driver.find_element_by_class_name('numInputWrapper')
    raw_input(self.util.get_text(el))

    self.year_button = self.container.find_element_by_class_name('react-datepicker__year-read-view--selected-year')
    self.current_year = self.year_button.text

########################### General ##############################

  def set_date(self, date):
    day = self.parse_date(date, 'day')
    month = self.parse_date(date, 'month')
    year = self.parse_date(date, 'year')
    self.load()
    # print('setting date')
    # print('day: ' + str(day))
    # print('month: ' + str(month))
    # print('year: ' + str(year))

    self.set_year(year)
    # raw_input('year?')
    self.set_month(month)
    # raw_input('month?')
    self.set_day(day)
    # raw_input('day?')

    # Wait for datepicker to disappear
    time.sleep(.4)

  def findIndices(self, s, character):
    return [i for i, letter in enumerate(s) if letter == character]

  def parse_date(self, dateStr, dateType):
    # Given dateStr "dd/mm/yyyy", parse and return month or year
    indices = self.findIndices(dateStr, '/')
    if len(indices) != 2:
      print('Invalid dateStr: ' + str(dateStr))

    # Convert month/day to int to strip off any leading 0's
    if dateType == 'month':
      return int(dateStr[:indices[0]])
    elif dateType == 'day':
      return int(dateStr[indices[0]+1:indices[1]])
    elif dateType == 'year':
      return dateStr[indices[1]+1:]

  def set_year(self, year):
    self.year_button.click()
    time.sleep(2)

    selectedYear = False
    count = 0
    while not selectedYear and count < 5:
      try:
        self.load_year_dropdown()
        # selected_year = self.container.find_element_by_class_name('react-datepicker__year-option--selected').text
        # print('selected year: ' + str(selected_year))

        # if year != selected_year:
        for i, option in enumerate(self.year_options):
          if i != 0:
            if option.text == year:
              option.click()
              selectedYear = True
              break
      except StaleElementReferenceException:
        # Often throws stale exception for no apparent reason
        print('unable to click year: ' + str(year) + '. ' + str(count))
      count += 1

  def load_year_dropdown(self):
    loaded = False
    count = 0
    while not loaded and count < 5:
      self.year_options = self.container.find_elements_by_class_name('react-datepicker__year-option')
      if len(self.year_options) > 20:
        loaded = True
      count += 1

  def set_month(self, month):
    current_month = self.read_current_month()
    # raw_input('current_month: ' + str(current_month))
    previous_button = self.container.find_element_by_class_name('react-datepicker__navigation--previous')
    next_button = self.container.find_element_by_class_name('react-datepicker__navigation--next')

    if current_month != month:
      correct_month = False
      count = 0
      while not correct_month and count < 12:
        if current_month > month:
          print('previous')
          previous_button.click()
        else:
          print('next')
          next_button.click()

        current_month = self.read_current_month()
        if current_month == month:
          correct_month = True
        count += 1

  def read_current_month(self):
    # Read text out of 'current month' text and return month's integer
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    text = self.container.find_element_by_class_name('react-datepicker__current-month').text
    spaceIndex = text.index(' ')
    month = text[:spaceIndex]
    monthInt = months.index(month)+1
    return monthInt

  def set_day(self, day):
    # Avoid trying to pick days from previous month
    startIndex = day-1
    day = str(day)
    setDay = False
    count = 0
    while not setDay and count < 5:
      try:
        dayEls = self.container.find_elements_by_class_name('react-datepicker__day')

        for dayEl in dayEls[startIndex:]:
          if dayEl.text == day:
            dayEl.click()
            setDay = True
            break
      except StaleElementReferenceException:
        # Often throws stale exception for no apparent reason
        print('unable to click day: ' + day + '. ' + str(count))
      count += 1








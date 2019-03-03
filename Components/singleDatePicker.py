from selenium.common.exceptions import (NoSuchElementException,
  ElementNotVisibleException, StaleElementReferenceException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
import time
import datetime
from utilityFuncs import UtilityFunctions

# flatpickr component: Datepicker for selecting Day/Month/Year.
# Used on Consent Form

# Currently only used for selecting current date.
# Only going to build out limited functionality (no changing month/year)
class SingleDatePicker():

  def __init__(self, driver):
    self.driver = driver
    self.util = UtilityFunctions(self.driver)
    self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    count = 0
    loaded = False
    while not loaded and count < 5:
      loaded = self.load()
      count += 1
      time.sleep(.2)


  def load(self):
    try:
      self.container = self.load_container()
      if self.container:
        self.month = self.container.find_element_by_class_name('cur-month')
        self.year = self.container.find_element_by_class_name('cur-year')
        self.day_cont = self.container.find_element_by_class_name('dayContainer')

        self.today = self.try_load_today()
        self.selected_day = self.try_load_selected_day()
        return True
      else:
        print('singleDatePicker: Could not find an open container')
      
    except NoSuchElementException:
      print('failed to load datepicker')
    return False

  def load_container(self):
    # For some reason has multiple 'months' of dates loaded. Month actually displayed is in last container
    containers = self.driver.find_elements_by_class_name('flatpickr-calendar')
    container = None
    for i, cont in enumerate(containers):
      classes = cont.get_attribute('class')
      if 'open' in classes:
        container = cont
    return container

  def try_load_today(self):
    # Won't have 'today' if input already has today's date or current month is not selected
    today = None
    try:
      today = self.day_cont.find_element_by_class_name('today')
    except NoSuchElementException:
      pass
    return today

  def try_load_selected_day(self):
    # May not have a day selected on displayed month (or at all)
    selectedEl = None
    try:
      selectedEl = self.day_cont.find_element_by_class_name('selected').text
    except NoSuchElementException:
      pass
    return selectedEl

########################### General ##############################

  def set_date(self, date):
    # Expects 'MM/DD/YYYY' format
    if date == 'current':
      self.set_current_date()
    else:
      self.set_year(date[-4:])
      # raw_input('set year?')
      self.set_month(date[:2])
      # raw_input('set month?')
      self.set_day(date[3:5])
      # raw_input('set day?')
    self.load()

  def set_current_date(self):
    now = datetime.datetime.now()
    self.set_date(now.strftime("%m/%d/%Y"))

  def get_date(self):
    # Return datepicker's value in MM/DD/YYYY format (current selection, not input value)
    # day will be '' if nothing is selected ('MM//YYYY')
    month = self.month_int(self.month.text)
    year = self.year.get_attribute('value')
    day = self.day_int(self.selected_day)
    
    date = month + '/' + day + '/' + year
    return {'month': month, 'year': year, 'day': day, 'date': date}

  def set_year(self, year):
    print('setting year: ' + str(year))
    current_year = self.year.get_attribute('value')
    count = 0
    while year != current_year and count < 50:
      if current_year > year: # 2018 > 2017
        year_down = self.container.find_element_by_class_name('arrowDown')
        self.util.click_el(year_down)
      elif current_year < year:
        year_up = self.container.find_element_by_class_name('arrowUp')
        self.util.click_el(year_up)
      time.sleep(.4)
      self.load()
      current_year = self.year.get_attribute('value')
      count += 1

  def set_month(self, month):
    print('setting month: ' + str(month))
    current_month = self.month_int(self.month.text)
    count = 0
    while current_month != month and count < 12:
      if current_month > month:
        print(str(current_month) + " > " + str(month))
        month_back = self.container.find_element_by_class_name('flatpickr-prev-month')
        self.util.click_el(month_back)
      elif current_month < month:
        print(str(current_month) + " < " + str(month))
        month_next = self.container.find_element_by_class_name('flatpickr-next-month')
        self.util.click_el(month_next)
      time.sleep(.4)
      self.load()
      current_month = self.month_int(self.month.text)
      count += 1

  def set_day(self, day):
    print('setting day: ' + str(day))
    errorFree = False
    count = 0
    while not errorFree and count < 10:
      try:
        days = self.day_cont.find_elements_by_class_name('flatpickr-day')
        for i, dayEl in enumerate(days):
          classes = dayEl.get_attribute('class')
          if 'nextMonthDay' not in classes and 'prevMonthDay' not in classes:
            # print(dayEl.text)
            if int(dayEl.text) == int(day):
              # print('clicking ' + dayEl.text)
              self.util.click_el(dayEl)
              errorFree = True
      except StaleElementReferenceException:
        print('failed to set day: ' + str(count))
      count += 1

  def validate_month(self, month):
    # Compare 'month' to picker's current month (MM format)
    matches = True
    # print('picker month: ' + str(self.month.text))
    # print('expected raw: ' + str(month))
    # print('expected parsed: ' + self.months[self])
    if self.months[month-1] != self.month.text:
      matches = False
    return matches

  def validate_day(self, day):
    # Compare 'day' to picker's current day (DD format)
    # Pass in None if not expecting a day selected
    # if self.selected_day:
    #   print('picker day: ' + str(self.selected_day.text))
    # else:
    #   print('picker day: None')
    # print('expected: ' + str(day))
    matches = False
    if day == self.selected_day or day == self.selected_day.text: # No day selected or values match
      matches = True
    return matches

  def validate_year(self, year):
    # Compare 'year' to picker's current year (YYYY format)
    # print('picker year: ' + str(self.year.get_attribute('value')))
    # print('expected year: ' + str(year))
    matches = True
    if self.year.get_attribute('value') != str(year):
      matches = False
    return matches

  def has_current_date(self):
    # Return 'current' if picker has today's date
    now = datetime.datetime.now()
    currentDate = 'current'
    now.strftime("%m/%d/%Y")

    if int(now.strftime("%Y")) != int(self.year.get_attribute('value')):
      print('Not current year: ' + str(now.strftime("%Y") + ', ' + str(self.year.get_attribute('value'))))
      currentDate = False
    if self.months[now.month-1] != self.month.text:
      print('Not current month: ' + self.months[now.month-1] + ', ' + str(self.month.text))
      currentDate = False
    if int(now.day) != int(self.selected_day):
      print('Not current day: ' + str(now.day) + ', ' + self.selected_day)
      currentDate = False
    return currentDate

  def month_int(self, value):
    # Given name of month, return string of name converted to integer (January = '01')
    return str(self.months.index(value)+1).zfill(2)

  def day_int(self, value):
    if value:
      return value.zfill(2)
    else:
      return ''


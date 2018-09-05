from utilityFuncs import UtilityFunctions

from selenium.common.exceptions import (NoSuchElementException,
  ElementNotVisibleException, StaleElementReferenceException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
import time

class DatePicker():
  """Date picker for MonthYear input"""

  def __init__(self, driver, container):
    self.driver = driver
    # Throw exception if container doesn't contain date stuff
    cont = container.find_element_by_class_name('Select--single')
    self.container = container
    self.util = UtilityFunctions(self.driver)

  def load(self, expectedState=None):
    try:
      # self.picker_state = self.get_picker_state()
      # if self.picker_state == 'wrong container':
      #   print('wrong datepicker container')
      #   return False
      # else:
      dropdownConts = self.container.find_elements_by_class_name('Select--single')
      if len(dropdownConts) < 2:
        print('not enough dropdown containers')
        return False

      self.month_cont = dropdownConts[0]
      self.year_cont = dropdownConts[1]


      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      print('failed to load datePicker')
      return False

  def get_picker_state(self):
    state = 'normal'
    # Make sure container has datePicker in it
    try:
      cont = self.container.find_element_by_class_name('Select--single')
    except NoSuchElementException:
      state = 'wrong container'
    return state


########################### General ##############################

  def set_date(self, date):
    month = self.parse_date(date, 'month')
    year = self.parse_date(date, 'year')
    self.load()
    print('setting date')
    print(month)
    print(year)
    WDW(self.driver, 10).until(lambda x: self.set_dropdown(self.month_cont, month))
    WDW(self.driver, 10).until(lambda x: self.set_dropdown(self.year_cont, year))

    # Wait for datepicker to disappear
    time.sleep(.4)

  def set_dropdown(self, container, value):
    # Figure out if you need to click 'Select-value-label' or 'Select-placeholder' element
    dropdown_preSet = False
    try:
      dropdown_value = container.find_element_by_class_name('Select-value-label')
      dropdown_placeholder = None
      dropdown_preSet = True
    except NoSuchElementException:
      dropdown_value = None
      dropdown_placeholder = container.find_element_by_class_name('Select-placeholder')

    # Only continue if value isn't already set
    if dropdown_value and self.util.get_text(dropdown_value) == value:
      return True

    # click it
    if dropdown_preSet:
      dropdown_value.click()
    else:
      dropdown_placeholder.click()
    # load options in dropdown
    options = {}
    count = 0
    loaded = False
    while not loaded and count < 5:
      try:
        menu = container.find_element_by_class_name('Select-menu-outer')
        divs = menu.find_elements_by_tag_name('div')
        for i, div in enumerate(divs):
          if i != 0:
            options[self.util.get_text(div).lower()] = divs[i]
        loaded = True
      except NoSuchElementException:
        print('Unable to find dropdown items for datepicker')
        count += 1

    if count == 5 or not options:
      print('Failed to load date dropdown options')
      return False

    # click option
    try:
      option = options[value.lower()]
      option.click()
      return True
    except (IndexError, KeyError) as e:
      print('invalid date option: ' + value)
      for option in options:
        print(option)

  def parse_date(self, dateStr, dateType):
    # Given dateStr "mm/yyyy", parse and return month or year
    divider = dateStr.index('/')
    # divider should always be 2
    if divider != 2:
      print('Trying to set invalid date: ' + str(dateStr))
    if dateType == 'month':
      months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      return months[int(dateStr[:divider]) - 1]
    else:
      year = dateStr[divider + 1:]
      return year

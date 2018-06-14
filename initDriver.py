from selenium import webdriver
import main

def get_desired_caps(browser):
  if browser.lower() == 'firefox':
    desired_caps = webdriver.DesiredCapabilities.FIREFOX
  elif browser.lower() == 'safari':
    desired_caps = webdriver.DesiredCapabilities.SAFARI
    safari_options = {'cleanSession': True}
    desired_caps['safariOptions'] = safari_options
  else:
    desired_caps = webdriver.DesiredCapabilities.CHROME
  return desired_caps

def start(browser=None):
  driver_url = 'http://127.0.0.1:5050/wd/hub'
  if browser is None:
    browser = 'chrome'

  desired_caps = get_desired_caps(browser)
  driver = webdriver.Remote(driver_url, desired_caps)

  # set default window settings
  driver.set_window_size(1200, 960)
  # driver.set_window_position(500, 0);
  if browser.lower() == 'safari':
    driver.maximize_window()

  return driver
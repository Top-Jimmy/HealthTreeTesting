from selenium.webdriver.chrome.options import Options
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

def get_chrome_options():
  #path = "/Users/andrewtidd/Library/Application Support/Google/Chrome/Default"
  options = Options()
  #options.add_argument("user-data-dir=" + path)
  if main.headless:
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
  return options

def start(browser=None):
  driver_url = 'http://127.0.0.1:5050/wd/hub'
  if browser is None:
    browser = 'chrome'

  desired_caps = get_desired_caps(browser)
  if browser == 'chrome':
    driver = webdriver.Chrome(chrome_options=get_chrome_options())
  else:
    driver = webdriver.Remote(driver_url, desired_caps)

  # set default window settings
  driver.set_window_size(1350, 950)
  driver.set_window_position(100, 0);
  if browser.lower() == 'safari':
    driver.maximize_window()

  return driver
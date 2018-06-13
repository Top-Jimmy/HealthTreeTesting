import main
from selenium.common.exceptions import (TimeoutException, WebDriverException,
	NoSuchElementException, StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW

class View:
	# super class for Views

	def __init__(self, driver):
		self.driver = driver

	def go(self, url=None):
		if url is None:
			url = main.base_url
			try:
				url = url + self.post_url
			except AttributeError:
				pass
		self.driver.get(url)
		return self.on()

	def on(self, arg1=None, arg2=None):
		wait_time = 10
		try:
			if arg1 is None:
				WDW(self.driver, wait_time).until(lambda x: self.load())
			elif arg2 is None:
				WDW(self.driver, wait_time).until(lambda x: self.load(arg1))
			else:
				WDW(self.driver, wait_time).until(lambda x: self.load(arg1, arg2))
			return True
		except TimeoutException:
			print 'Failed to load: ' + str(self.__class__)
			return False

	def move_to_el(self, el, click=True):
		self.driver.execute_script('arguments[0].scrollIntoView();', el)
		time.sleep(.6)
		if click:
			try:
				el.click()
				return True
			except WebDriverException:
				pass
		return False

	def readErrors(self):
		# Return any errors displaying
		try:
			cont = self.driver.find_element_by_class_name('s-alert-wrapper')
			if len(cont.text) > 0:
				return self.createErrorObj(cont.text.lower())
		except (NoSuchElementException, StaleElementReferenceException) as e:
			pass
		return None





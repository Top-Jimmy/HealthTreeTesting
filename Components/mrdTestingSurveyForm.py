from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class MrdTestingSurveyForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		form = self.driver.find_elements_by_class_name('form')[-2]
		
		self.load_questions()
		# return self.validate()
		return True

	# def load_questions(self):

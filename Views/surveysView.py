from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import menu
from Components import header
from Components import conditionsSurveyForm
from Components import multipleMyelomaSurveyForm
from Components import imagingSurveyForm
from Components import vaccinationsSurveyForm
from Components import mrdTestingSurveyForm
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SurveysView(view.View):
	post_url = 'surveys'

	def load(self):
		self.menu = menu.Menu(self.driver)
		self.header = header.AuthHeader(self.driver)

		self.form = self.driver.find_element_by_id('page-content-wrapper')

		self.continue_button = self.form.find_element_by_tag_name('a')

		self.load_surveys()

		# self.validate()
		return True
		

	def load_surveys(self):
		self.surveys = []
		surveyButtons = {}
		surveys = self.form.find_elements_by_class_name('survey-div')
		for survey in surveys:
			span = survey.find_element_by_tag_name('span')
			key = span.text[1:-1]
			surveyButton = survey.find_element_by_tag_name('button')
			surveyButtons[key.lower()] = surveyButton

		self.surveys.append(surveyButtons)

		return self.surveys


	def conditions_survey(self, conditionsInfo, action='cancel'):
		self.precursor_button.click()
		self.conditionsSurveyForm = conditionsSurveyForm.ConditionsSurveyForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.conditionsSurveyForm.load())
		self.conditionsSurveyForm.submit(conditionsInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def molecular_survey(self, myelomaInfo, action='cancel'):
		self.genetic_button.click()
		self.multipleMyelomaSurveyForm = multipleMyelomaSurveyForm.MultipleMyelomaSurveyForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.multipleMyelomaSurveyForm.load())
		self.multipleMyelomaSurveyForm.submit(myelomaInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def imaging_survey(self, imagingInfo, action='cancel'):
		self.imaging_button.click()
		self.imagingSurveyForm = imagingSurveyForm.ImagingSurveyForm(self.driver)
		WDW(self.driver, 10).until(lambda x: self.imagingSurveyForm.load())
		self.imagingSurveyForm.submit(imagingInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))


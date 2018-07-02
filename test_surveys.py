import unittest
import main
import initDriver
import profiles
import time

class TestSurveys(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		'''surveys : surveys . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		surveysView = self.andrew.surveysView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Surveys')
		
		self.assertTrue(surveysView.on())

	def test_conditions_survey(self):
		'''Surveys : Surveys . test_conditions_survey'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		surveysView = self.andrew.surveysView

		conditionsInfo = {
			'participate': 'yes'
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Surveys')
		
		self.assertTrue(surveysView.on())
		surveysView.conditions_survey(conditionsInfo, 'cancel')

	def test_molecular_survey(self):
		'''Surveys : Surveys . test_molecular_survey'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		surveysView = self.andrew.surveysView

		myelomaInfo = {
			'fish': True,
			'cytogenetics': True,
			'gep': False,
			'ngs': False,
			'idk': False,
			'none': False,
			'since_fish': True,
			'since_cytogenetics': False,
			'since_gep': True,
			'since_ngs': False,
			'since_idk': False,
			'since_none': False,
			'comment': 'New Orleans'
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Surveys')

		self.assertTrue(surveysView.on())
		surveysView.molecular_survey(myelomaInfo, 'cancel')
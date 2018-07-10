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
			'gep': True,
			'ngs': True,
			'idk': True,
			'none': True,
			'since_fish': True,
			'since_cytogenetics': True,
			'since_gep': True,
			'since_ngs': True,
			'since_idk': True,
			'since_none': True,
			'comment': 'New Orleans',
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Surveys')

		self.assertTrue(surveysView.on())
		surveysView.molecular_survey(myelomaInfo, 'cancel')
		self.assertTrue(surveysView.on())

	def test_imaging_survey(self):
		'''Surveys : Surveys . test_imaging_survey'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		surveysView = self.andrew.surveysView

		imagingInfo = {
			'xray': True,
			'wbldct': True,
			'spinal': True,
			'whole_mri': True,
			'bonescan': True,
			'petct': True,
			'petmri': True,
			'bone_density': True,
			'since_xray': True,
			'since_wbldct': True,
			'since_spinal': True,
			'since_whole_mri': True,
			'since_bonescan': True,
			'since_petct': True,
			'since_petmri': True,
			'since_bone_density': True,
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Surveys')

		self.assertTrue(surveysView.on())
		surveysView.imaging_survey(imagingInfo, 'cancel')
		self.assertTrue(surveysView.on())
import unittest
import main
import initDriver
import profiles


class TestAboutMe(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		'''test_aboutMe.py:TestAboutMe.test_navigate '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Myeloma Diagnosis')

	def test_validate(self):
		'''test_aboutMe.py:TestAboutMe.test_validate '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on(self.andrew.credentials['about_me_data']))

	def test_warnings(self):
		'''test_aboutMe.py:TestAboutMe.test_warnings '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		about_me_data = self.andrew.credentials['about_me_data']
		about_me_data['treatment_goals'] = ''
		expectedWarnings = ['Missing treatement goals']

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())

	def test_tooltip(self):
		'''test_aboutMe.py:TestAboutMe.test_tooltip '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.aboutMeForm.tooltip()


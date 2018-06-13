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
		'''AboutMe : AboutMe . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Myeloma Diagnosis')

	def test_validate(self):
		'''AboutMe : AboutMe . test_validate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on(self.andrew.credentials['about_me_data']))

	def test_warnings(self):
		'''AboutMe : AboutMe . test_warnings'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		about_me_data = self.andrew.credentials['about_me_data']
		about_me_data['first_name'] = ''
		expectedWarnings = ['Missing first name']


		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())

		self.assertTrue(aboutMeView.submit(about_me_data, expectedWarnings=expectedWarnings))



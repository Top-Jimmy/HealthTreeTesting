import unittest
import main
import initDriver
import profiles

class TestCurrentHealth(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		'''CurrentHealth : CurrentHealth . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		currentHealthView = self.andrew.currentHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Current Health')
		self.assertTrue(currentHealthView.on())

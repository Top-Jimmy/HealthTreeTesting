import unittest
import main
import initDriver
import profiles

class TestMyelomaLabs(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		'''MyelomaGenetics : MyelomaGenetics . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaLabsView = self.andrew.myelomaLabsView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Labs')
		self.assertTrue(myelomaLabsView.on())
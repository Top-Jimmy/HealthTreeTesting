import unittest
import main
import initDriver
import profiles

class TestGetMyLabs(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		''' test_get_my_labs.py:TestGetMyLabs.test_navigate '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaLabsView = self.andrew.myelomaLabsView
		myLabs_facilities = self.andrew.myLabsFacilitiesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Labs')
		self.assertTrue(myelomaLabsView.on())
		myelomaLabsView.get_my_labs()
		self.assertTrue(myLabs_facilities.on())

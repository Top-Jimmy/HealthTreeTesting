import unittest
import main
import initDriver
import profiles
import time

class TestFullHealth(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		'''Full Health Profile : Full Health Profile . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		fullHealthView = self.andrew.fullHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Full Health Profile')
		
		self.assertTrue(fullHealthView.on('My Myeloma'))

		self.assertTrue(fullHealthView.select_tab('demographics'))

		self.assertTrue(fullHealthView.select_tab('full health history'))

		self.assertTrue(fullHealthView.select_tab('family history'))

		self.assertTrue(fullHealthView.select_tab('lifestyle'))

		self.assertTrue(fullHealthView.select_tab('quality of life'))

		self.assertTrue(fullHealthView.select_tab('summary'))

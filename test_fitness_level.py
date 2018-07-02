import unittest
import main
import initDriver
import profiles
import copy 

class TestFitnessLevel(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def test_navigate(self):
		'''FitnessLevel : FitnessLevel . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		fitLvlView = self.andrew.fitLvlView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Fitness Level')
		self.assertTrue(fitLvlView.on())

	def test_submit(self):
		'''FitnessLevel : FitnessLevel . test_submit'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		fitLvlView = self.andrew.fitLvlView

		fitnessInfo = [
			True,
		]

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Fitness Level')
		self.assertTrue(fitLvlView.on())

		fitLvlView.fitLvlForm.submit(fitnessInfo)




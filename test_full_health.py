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
		
		self.assertTrue(fullHealthView.on('my myeloma'))

		self.assertTrue(fullHealthView.select_tab('demographics'))

		self.assertTrue(fullHealthView.select_tab('full health history'))

		self.assertTrue(fullHealthView.select_tab('family history'))

		self.assertTrue(fullHealthView.select_tab('lifestyle'))

		self.assertTrue(fullHealthView.select_tab('quality of life'))

		self.assertTrue(fullHealthView.select_tab('full health profile summary'))


	def test_myeloma_form(self):
		''' test_full_health.py:TestFullHealth.test_myeloma_form '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		fullHealthView = self.andrew.fullHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Full Health Profile')
			
		self.assertTrue(fullHealthView.on('my myeloma'))

		form_data = [
			[{'option': 'iga lambda'}, {'option': 'yes'}, {'option': 'no'}],
			[{'option': 'yes'}],
			[{'option': 'yes'}, {'option': 'yes'}, {'option': 'yes'}, {'option': 'yes'}, {'option': 'yes'}, {'option': 'yes'}],
			[{'option': 'yes'}, {'option': 'yes'}, {'option': 'yes'}],
		]

		self.assertTrue(fullHealthView.submit(form_data))

	def test_demographics_form(self):
		''' test_full_health.py:TestFullHealth.test_demographics_form '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		fullHealthView = self.andrew.fullHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Full Health Profile')

		self.assertTrue(fullHealthView.on('my myeloma'))

		form_data = [
			[{'option': 'White (Original ancestry from Europe, Middle East, North Africa)'}, {'option': 'Hispanic or Latino'}, {'dropdown': 'Cuban'}, {'dropdown': 'Albania'}, {'option': 'Gilford'}, {'option': 'Sandy'}, {'option': 'Sandy'}, {'dropdown': 'None'}, {'dropdown': 'Married'}, {'dropdown': 'Some grade school'}, {'dropdown': 'Disabled'}, {'option': 'yes'}, {'option': 'yes'}]
		]

		self.assertTrue(fullHealthView.select_tab('demographics'))

		self.assertTrue(fullHealthView.submit(form_data))


	def test_health_history_form(self):
		''' test_full_health.py:TestFullHealth.test_health_history_form '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		fullHealthView = self.andrew.fullHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Full Health Profile')
		
		self.assertTrue(fullHealthView.on('my myeloma'))

		self.assertTrue(fullHealthView.select_tab('full health history'))

		form_data = [
			[{'option': 'wheat'}, {'option': 'no'}, {'option': 'household pest'}, {'option': 'bandages'}, {'option': 'indoor molds'}, {'option': 'cats'}, {'option': 'grass'}],
			[{'option': 'liver'}],
			[{'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}]
		]

		self.assertTrue(fullHealthView.submit(form_data))


	def test_quality_form(self):
		''' test_full_health.py:TestFullHealth.test_quality_form '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		fullHealthView = self.andrew.fullHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Full Health Profile')
		
		self.assertTrue(fullHealthView.on('my myeloma'))

		form_data = [
			[{'option': 'somewhat'}, {'option': 'quite a bit'}, {'option': 'very much'}],
			[{'option': 'quite a bit'}, {'option': 'not at all'}, {'option': 'not at all'}, {'option': 'a little bit'}, {'option': 'somewhat'}, {'option': 'very much'}],
			[{'option': 'quite a bit'}, {'option': 'not at all'}, {'option': 'not at all'}, {'option': 'a little bit'}, {'option': 'somewhat'}, {'option': 'very much'}],
			[{'option': 'quite a bit'}, {'option': 'not at all'}, {'option': 'not at all'}, {'option': 'a little bit'}, {'option': 'somewhat'}, {'option': 'very much'}],
			[{'option': 'quite a bit'}, {'option': 'not at all'}, {'option': 'not at all'}, {'option': 'a little bit'}, {'option': 'somewhat'}, {'option': 'very much'}, {'option': 'quite a bit'}, {'option': 'not at all'}, {'option': 'not at all'}, {'option': 'a little bit'}, {'option': 'somewhat'}],
			[{'option': 'no'}]
		]
		self.assertTrue(fullHealthView.select_tab('quality of life'))

		self.assertTrue(fullHealthView.submit(form_data))


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
			[{'option': 'no'}, {'option': 'iga lambda'}, {'option': 'no'}, {'option': 'no'}],
			[{'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'yes', 'secondary': {'text': 'Hello'}}, 
			 {'option': 'no'}, {'option': 'no'}],
			[{'option': 'no'}, {'option': 'no'}, {'option': 'no'}],
		]

		self.assertTrue(fullHealthView.submit(form_data, 'my myeloma'))

		self.assertTrue(fullHealthView.on('my myeloma'))

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
			[{'option': 'white (original ancestry from europe, middle east, north africa)'}, {'option': 'hispanic or latino'}, {'dropdown': 'Cuban'}, {'dropdown': 'Albania'}, {'option': 'gilford'}, {'option': 'sandy'}, {'option': 'sandy'}, {'dropdown': 'None'}, {'dropdown': 'Married'}, {'dropdown': 'Some grade school'}, {'dropdown': 'Disabled'}, {'option': 'yes'}, {'option': 'yes'}]
		]

		self.assertTrue(fullHealthView.select_tab('demographics'))

		self.assertTrue(fullHealthView.submit(form_data, 'demographics'))


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
			[{'option': 'eggs'}, {'option': 'no'}, {'option': 'household pest'}, {'option': 'other', 'secondary': {'text': 'cheezits'}}, {'option': 'indoor molds'}, {'option': 'cats'}, {'option': 'grass'}],
			[{'option': 'liver', 'secondary': {'text': 'never'}}],
			[{'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}]
		]

		self.assertTrue(fullHealthView.submit(form_data, 'full health history'))


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
			[{'option': 'yes', 'secondary': {'options': 'loss of income'}}]
		]
		self.assertTrue(fullHealthView.select_tab('quality of life'))

		self.assertTrue(fullHealthView.submit(form_data, 'quality of life'))


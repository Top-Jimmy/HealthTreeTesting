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

		# self.assertTrue(fullHealthView.select_tab('full health profile summary'))


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
			[{'option': 'White (Original ancestry from Europe, Middle East, North Africa)'}, {'option': 'Hispanic or Latino'}, {'multiple_dropdown': 'Cuban'}, {'dropdown': 'United States of America'}, {'textInput': 'gilford'}, {'textInput': 'sandy'}, {'textInput': 'sandy'}, {'dropdown': 'None'}, {'dropdown': 'Married'}, {'dropdown': 'Some grade school'}, {'dropdown': 'Disabled'}, {'option': 'Yes', 'secondary': {'options': 'Insurance through work'}}, {'option': 'No'}]
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

	def test_family_history_form(self):
		'''test_full_health:TestFullHealth.test_family_history_form'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		fullHealthView = self.andrew.fullHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Full Health Profile')

		self.assertTrue(fullHealthView.on('my myeloma'))

		self.assertTrue(fullHealthView.select_tab('family history'))

		form_data = [
			[{'multiple_dropdown': 'colon'}, {'multiple_dropdown': 'unknown'}, {'multiple_dropdown': 'breast'}, {'multiple_dropdown': 'breast'}, {'multiple_dropdown': 'colorectal'}, {'multiple_dropdown': 'prostate'}, {'multiple_dropdown': 'brain'}],
			[{'option': 'no'}, {'option': 'no'}, {'option': 'no'}],
			[{'option': 'yes', 'secondary': {'options': 'first cousin'}}, {'option': 'no'}, {'option': 'no'}]
		]

		self.assertTrue(fullHealthView.submit(form_data, 'family history'))

	def test_lifestyle_form(self):
		''' test_full_health.py:TestFullHealth.test_lifestyle_form '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		fullHealthView = self.andrew.fullHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Full Health Profile')

		self.assertTrue(fullHealthView.on('my myeloma'))

		form_data = [
			[{'option': 'no'}],
			[{'option': 'no'}, {'option': 'cigars'}],
			[{'option': 'no'}],
			[{'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'option': 'no'}, {'textInput': 'no'}],
			[{'textInput': '5.7'}, {'textInput': '156'}, {'textInput': '153'}, {'textInput': '134'}],
			[{'dropdown': '3 - 4 hours'}, {'dropdown': '5 - 6 hours'}],
			[{'multiple_dropdown': 'curcumin (tumeric)'}, {'multiple_dropdown': 'vitamin e'}],
			[{'option': 'personal prayer'}],
			[{'dropdown': 'both religious and spiritual.'}],
			[{'textInput': 'no'}]
		]

		self.assertTrue(fullHealthView.select_tab('lifestyle'))

		self.assertTrue(fullHealthView.submit(form_data, 'lifestyle'))

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


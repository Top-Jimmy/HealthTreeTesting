import unittest
import main
import initDriver
import profiles
import time

class TestMyelomaDiagnosis(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_fresh_form(self):
		'''MyelomaDiagnosis : MyelomaDiagnosis . test_submit'''
		# User submits fresh form, then verifies saved form loads and has expectedValues
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		formData =  {
			'newly_diagnosed': 'no',
			'diagnosis_date': '05/2018',
			'first_diagnosis': 'plasmacytoma',
			'high_risk': 'no',
			'transplant_eligible': 'no',
			'bone_lesions': 'no lesions',
			'diagnosis_location': {
				'facility': 'Huntsman Cancer',
				'city': 'Salt Lake City',
				'state': 'Utah',
			},
			'additional_diagnosis': False,
			'additional_diagnoses': [], # i.e. [{'date': '01/2000', 'diagnosis': 'Smoldering Myeloma'},]
			'physicians': [
				{'name': 'David Avigan',
					'facility': 'Beth Israel Deaconess Medical Center',
					'city': 'Boston',
					'state': 'Massachusetts',
				},
			],
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Myeloma Diagnosis')

		self.assertTrue(myelDiagView.on('fresh'))
		self.assertTrue(myelDiagView.submitFreshForm(formData))

	def test_saved_form(self):
		'''MyelomaDiagnosis : MyelomaDiagnosis . test_saved_form'''
		# User already has fresh form submitted. Saved form loads and has expectedValues
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Myeloma Diagnosis')

		self.assertTrue(myelDiagView.on('saved'))

	def test_typeahead(self):
		'''MyelomaDiagnosis : MyelomaDiagosis . test_typeahead'''
		# Physician name field will suggest options as user types. Tab will autofill physician fields
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))





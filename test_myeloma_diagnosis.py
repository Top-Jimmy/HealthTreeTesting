import unittest
import main
import initDriver
import profiles
import time

class TestMyelomaDiagnosis(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')
		self.elliot = profiles.Profile(self.driver, 'elliot')

	def tearDown(self):
		self.driver.quit()

	def test_additional_physicians(self):
		'''MyelomaDiagnosis : MyelomaDiagnosis . test_additional_physicians'''
		# Fresh and Saved form: Test adding, editing and deleting multiple physicians
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		formInfo =  {
			'newly_diagnosed': 'no',
			'diagnosis_date': '05/2018',
			'type': 'plasmacytoma',
			'high_risk': 'no',
			'transplant_eligible': 'no',
			'lesions': 'no lesions',
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
				{'name': 'Kenneth Anderson',
					'facility': 'Dana Farber Cancer Institute',
					'city': 'Brookline',
					'state': 'Massachusetts',
				},
				{'name': 'Tomer Mark',
					'facility': 'Weill Cornell Medicine Myeloma Center',
					'city': 'New York City',
					'state': 'New York',
				},
			],
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Myeloma Diagnosis')

		self.assertTrue(myelDiagView.on('fresh'))
		self.assertTrue(myelDiagView.myelomaDiagnosisFreshForm.submit(formInfo, False))




	def test_fresh_form(self):
		'''MyelomaDiagnosis : MyelomaDiagnosis . test_submit'''
		# User submits fresh form, then verifies saved form loads and has expectedValues
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		formInfo =  {
			'newly_diagnosed': 'no',
			'diagnosis_date': '05/2018',
			'type': 'plasmacytoma',
			'high_risk': 'no',
			'transplant_eligible': 'no',
			'lesions': 'no lesions',
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
		self.assertTrue(myelDiagView.submitFreshForm(formInfo))
		myelDiagView.myelomaDiagnosisSavedForm.delete_diagnosis()

		self.assertTrue(myelDiagView.on('fresh'))

	def test_saved_form(self):
		'''MyelomaDiagnosis : MyelomaDiagnosis . test_saved_form'''
		# User already has fresh form submitted. Saved form loads and has expectedValues
		homeView = self.elliot.homeView
		aboutMeView = self.elliot.aboutMeView
		myelDiagView = self.elliot.myelomaDiagnosisView

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.elliot.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Myeloma Diagnosis')

		self.assertTrue(myelDiagView.on('saved', self.elliot.credentials['myeloma_diagnosis_data']))

	def test_typeahead(self):
		'''MyelomaDiagnosis : MyelomaDiagosis . test_typeahead'''
		# Physician name field will suggest options as user types. Tab will autofill physician fields
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		physicianInfo = {'name': 'David Avigan',
			'facility': 'Beth Israel Deaconess Medical Center',
			'city': 'Boston',
			'state': 'Massachusetts',
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Myeloma Diagnosis')
		self.assertTrue(myelDiagView.on('fresh'))

		myelDiagView.myelomaDiagnosisFreshForm.add_physician_typeahead('David', 'David Avigan', physicianInfo)




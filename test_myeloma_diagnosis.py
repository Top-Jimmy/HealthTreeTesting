import unittest
import main
import initDriver
import profiles
import time
import copy

class TestMyelomaDiagnosis(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')
		self.elliot = profiles.Profile(self.driver, 'elliot')

	def tearDown(self):
		self.driver.quit()

	def test_additional_diagnoses(self):
		'''MyelomaDiagnosis : MyelomaDiagnosis . test_additional_diagnoses'''
		# Fresh and Saved form: Test adding, editing and deleting multiple diagnoses
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
			'additional_diagnosis': True,
			'additional_diagnoses': [
				{'date': '01/2000', 'type': 'Smoldering Myeloma'},
				{'date': '12/2004', 'type': 'Multiple myeloma and amyloidosis'},
			], # i.e. [{'date': '01/2000', 'diagnosis': 'Smoldering Myeloma'},]
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
		self.assertTrue(myelDiagView.myelomaDiagnosisFreshForm.submit(formInfo, False))




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
		'''MyelomaDiagnosis : MyelomaDiagnosis . test_fresh_form'''
		# User submits fresh form, then verifies saved form loads and has expectedValues
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		david = {
			'name': 'David Avigan',
			'facility': 'Beth Israel Deaconess Medical Center',
			'city': 'Boston',
			'state': 'Massachusetts',
		}
		tomer = {
			'name': 'Tomer Mark',
			'facility': 'Weill Cornell Medicine Myeloma Center',
			'city': 'New York City',
			'state': 'New York',
		}
		kenneth = {
			'name': 'Kenneth Anderson',
			'facility': 'Dana Farber Cancer Institute',
			'city': 'Brookline',
			'state': 'Massachusetts',
		}

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
			'physicians': [david, tomer],
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Myeloma Diagnosis')

		self.assertTrue(myelDiagView.on('fresh'))
		self.assertTrue(myelDiagView.submitFreshForm(formInfo))

		# Add a third physician. Then delete 2 of the 3

		myelDiagView.add_physician(kenneth, {'meta': [{'num_physicians': 3}]})
		myelDiagView.delete('physician', 2, {'meta': [{'num_physicians': 2}]})
		myelDiagView.delete('physician', 1, {'meta': [{'num_physicians': 1}]})

		# Delete diagnosis and reload fresh form
		myelDiagView.delete('diagnosis', 0)

	def test_saved_form(self):
		'''MyelomaDiagnosis : MyelomaDiagnosis . test_saved_form'''
		# User already has fresh form submitted. Saved form loads and has expectedValues
		homeView = self.elliot.homeView
		aboutMeView = self.elliot.aboutMeView
		myelDiagView = self.elliot.myelomaDiagnosisView
		default_diagnosis = self.elliot.credentials['myeloma_diagnosis_data']

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.elliot.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Myeloma Diagnosis')

		self.assertTrue(myelDiagView.on('saved', default_diagnosis))

		# Edit diagnosis. Check that changes are reflected on saved form
		edited_diagnosis = copy.deepcopy(default_diagnosis)
		location = default_diagnosis['diagnosis_location']
		edited_diagnosis['diagnosis_date'] = '05/2018'
		edited_diagnosis['lesions'] = '6 or more'
		edited_diagnosis['diagnosis_location']['city'] = 'Logan'
		edited_diagnosis['diagnosis_date'] = '04/2018'
		myelDiagView.myelomaDiagnosisSavedForm.edit_diagnosis(edited_diagnosis)
		self.assertTrue(myelDiagView.on('saved', edited_diagnosis))
		raw_input('edited?')
		# reset diagnosis back to original info
		myelDiagView.myelomaDiagnosisSavedForm.edit_diagnosis(default_diagnosis)
		self.assertTrue(myelDiagView.on('saved', default_diagnosis))

		# Add a few diagnoses, then delete them
		edited_diagnosis = copy.deepcopy(default_diagnosis)
		additional_diagnoses = [
			{'date': '01/2000', 'type': 'Multiple Myeloma'},
			{'date': '06/2012', 'type': 'Primary Plasma Cell Leukemia (PCL)'},
		]
		edited_diagnosis['additional_diagnoses'] = additional_diagnoses

		myelDiagView.add_diagnosis(additional_diagnoses[0], {'meta': [{'num_diagnoses': 2}]})
		myelDiagView.add_diagnosis(additional_diagnoses[1], {'meta': [{'num_diagnoses': 3}]})
		self.assertTrue(myelDiagView.on('saved', edited_diagnosis))

		myelDiagView.delete('diagnosis', 2, {'meta': [{'num_diagnoses': 2}]})
		myelDiagView.delete('diagnosis', 1, {'meta': [{'num_diagnoses': 1}]})
		self.assertTrue(myelDiagView.on('saved', default_diagnosis))

		# Add a few physicians, then delete them

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




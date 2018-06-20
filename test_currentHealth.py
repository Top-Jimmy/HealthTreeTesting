import unittest
import main
import initDriver
import profiles

class TestCurrentHealth(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		'''CurrentHealth : CurrentHealth . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		currentHealthView = self.andrew.currentHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Current Health')
		self.assertTrue(currentHealthView.on())

	def test_recently_diagnosed(self):
		'''CurrentHealth : CurrentHealth . test_recently_diagnosed'''
		# Andrew: Go to 'Current Health'. Should not have first 3 questions (no saved diagnosis)
		# Go to 'Myeloma Diagnosis' and save diagnosis that is not recent
		# Continue on to 'Current Health' and verify all questions are there

		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		currentHealthView = self.andrew.currentHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Current Health')
		# todo: verify it does not have 3 questions
		expectedValues = {
			'meta': [
				{'num_questions': 8},
			],
		}
		self.assertTrue(currentHealthView.on(expectedValues))

		# Submit non-recent Diagnosis
		currentHealthView.menu.go_to('Myeloma Diagnosis')
		self.assertTrue(myelDiagView.on('fresh'))
		freshFormInfo = {
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
			'additional_diagnoses': [],
			'physicians': [
				{'name': 'David Avigan',
					'facility': 'Beth Israel Deaconess Medical Center',
					'city': 'Boston',
					'state': 'Massachusetts',
				},
			],
		}
		self.assertTrue(myelDiagView.submitFreshForm(freshFormInfo))
		myelDiagView.myelomaDiagnosisSavedForm.continue_button.click()

		# Should have first 3 questions + 8 default questions
		currentQuestions = [
			{'name': 'Is your myeloma currently stable?',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Are your M-protein or light chains moving up (relapsing)?',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Do you have recent issues with pain, anemia, elevated calcium or bone pain?',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
		]
		defaultQuestions =  [
			{'name': 'Heart Conditions',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Lung Conditions',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Kidney Conditions',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Diabetes Conditions',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Blood Pressure Conditions',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Blood Clot (DVT) Conditions',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Neuropathy Conditions',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Other Health Conditions',
				'value': 'dont know',
				'secondaryQuestions': [],
			},
		]
		# formInfo = {
		# 	'questions': currentQuestions + defaultQuestions,
		# 	'meta': [{'num_questions': 11}],
		# }
		formInfo = {
			'questions': defaultQuestions,
			'meta': [{'num_questions': 8}],
		}
		self.assertTrue(currentHealthView.on(formInfo))
		self.assertTrue(currentHealthView.submit(formInfo))





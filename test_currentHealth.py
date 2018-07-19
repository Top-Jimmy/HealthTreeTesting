import unittest
import main
import initDriver
import profiles
import copy # copy.deepcopy(object)

class TestCurrentHealth(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

		self.defaultQuestions =  [
			{'name': 'Heart Conditions', 'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Lung Conditions', 'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Kidney Conditions', 'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Diabetes Conditions', 'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Blood Pressure Conditions', 'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Blood Clot (DVT) Conditions', 'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Neuropathy Conditions', 'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Other Health Conditions', 'value': 'dont know',
				'secondaryQuestions': [],
			},
		]

		self.freshFormInfo = {
			# 'newly_diagnosed': 'No',
			'diagnosis_date': '05/2018',
			'type': 'solitary plasmacytoma',
			'stable': 'no',
			'm_protein': 'no',
			'recent_pain': 'yes',
			'lesions': 'no lesions',
			'high_risk': 'no',
			'transplant_eligible': 'no',
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

	def test_non_recent_diagnosis(self):
		'''CurrentHealth : CurrentHealth . test_non_recent_diagnosis'''
		# Andrew: 'Current Health' should no longer have 3 extra questions for non-recent diagnoses (Not for MGUS or smoldering)
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		currentHealthView = self.andrew.currentHealthView
		fitLvlView = self.andrew.fitLvlView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		# Should have 8 questions w/ no diagnosis saved
		aboutMeView.menu.go_to('Current Health')
		expectedValues = {
			'meta': {'num_questions': 8},
		}
		self.assertTrue(currentHealthView.on(expectedValues))

		# Submit non-recent Diagnosis
		currentHealthView.menu.go_to('Myeloma Diagnosis')
		self.assertTrue(myelDiagView.on('fresh'))
		self.assertTrue(myelDiagView.submitFreshForm(self.freshFormInfo))
		myelDiagView.myelomaDiagnosisSavedForm.continue_button.click()

		# Should still have 8 questions
		formInfo = {
			'questions': self.defaultQuestions,
			'meta': {'num_questions': 8},
		}
		self.assertTrue(currentHealthView.on(formInfo))
		self.driver.refresh()
		self.assertTrue(currentHealthView.on(formInfo))
		self.assertNotEquals(currentHealthView.menu.selected_option(), 'Current Health')
		self.assertTrue(currentHealthView.submit(formInfo))

		# Reset: Delete Diagnosis
		self.assertTrue(fitLvlView.on())
		fitLvlView.menu.go_to('Myeloma Diagnosis')
		self.assertTrue(myelDiagView.on('saved', {'meta': {'num_diagnoses': 1}} ))
		myelDiagView.delete('diagnosis', 0)

	def test_secondary_questions(self):
		'''CurrentHealth : CurrentHealth . test_secondary_questions'''
		# CurrentHealth should be able to set and read correct values for secondary questions
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		currentHealthView = self.andrew.currentHealthView
		fitLvlView = self.andrew.fitLvlView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Current Health')

		# Should not have a diagnosis saved. Therefore should get all questions
		defaultFormInfo = {
			'questions': self.defaultQuestions,
			'meta': {'num_questions': 8},
		}
		self.assertTrue(currentHealthView.on(defaultFormInfo))

		# Update a few secondary questions and verify form has expected changes
		heartConditions = {
			'name': 'Heart Conditions',
			'value': 'yes',
			'secondaryQuestions': [
				{'Heart disease but not heart failure': False},
				{'History of heart failure but well controlled': False},
				{'Ongoing heart failure': True}
			]
		}
		lungConditions = {
			'name': 'Lung Conditions',
			'value': 'yes',
			'secondaryQuestions': [
				{'Known lung disease and difficulty breathing when exercising': False},
				{'Known lung disease and difficulty breathing when resting': False},
			]
		}
		kidneyConditions = {
			'name': 'Kidney Conditions',
			'value': 'yes',
			'secondaryQuestions': [
				{'Mild kidney problems (renal impairment)': True},
				{'Severe kidney problems or on dialysis': True},
			]
		}
		updatedQuestions = copy.deepcopy(self.defaultQuestions)
		updatedQuestions[0] = heartConditions
		updatedQuestions[1] = lungConditions
		updatedQuestions[2] = kidneyConditions
		updatedFormInfo = {
			'questions': updatedQuestions,
			'meta': {'num_questions': 8},
		}
		currentHealthView.currentHealthForm.answer_question(0, heartConditions)
		currentHealthView.currentHealthForm.answer_question(1, lungConditions)
		currentHealthView.currentHealthForm.answer_question(2, kidneyConditions)
		self.assertTrue(currentHealthView.on(updatedFormInfo))

		# Reset to default answers (I don't know for everything)
		self.assertTrue(currentHealthView.submit(defaultFormInfo))

	def test_tooltip(self):
		'''CurrentHealth : CurrentHealth . test_tooltip'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		currentHealthView = self.andrew.currentHealthView
		
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Current Health')
		self.assertTrue(currentHealthView.on())
		currentHealthView.currentHealthForm.tooltip()


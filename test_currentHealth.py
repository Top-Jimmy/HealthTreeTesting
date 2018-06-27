import unittest
import main
import initDriver
import profiles
import copy # copy.deepcopy(object)

class TestCurrentHealth(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

		# Should get currentQuestions when either...
		# 1. Have not saved a diagnosis
		# 2. Diagnosis is not 'recently diagnosed'
		self.currentQuestions = [
			{'name': 'Is your myeloma currently stable?', 'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Are your M-protein or light chains moving up (relapsing)?', 'value': 'dont know',
				'secondaryQuestions': [],
			},
			{'name': 'Do you have recent issues with pain, anemia, elevated calcium or bone pain?', 'value': 'dont know',
				'secondaryQuestions': [],
			},
		]
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
			'diagnosis_date': '05/2016',
			'type': 'solitary plasmacytoma',
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
		# Andrew: Go to 'Current Health'. Should have first 3 questions (no saved diagnosis)
		# Go to 'Myeloma Diagnosis' and save diagnosis that is not recent
		# Continue on to 'Current Health' and verify all questions are there

		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		currentHealthView = self.andrew.currentHealthView
		fitLvlView = self.andrew.fitLvlView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Current Health')
		expectedValues = {
			'meta': [
				{'num_questions': 8},
			],
		}
		self.assertTrue(currentHealthView.on(expectedValues))

		# Submit non-recent Diagnosis
		currentHealthView.menu.go_to('Myeloma Diagnosis')
		self.assertTrue(myelDiagView.on('fresh'))

		self.assertTrue(myelDiagView.submitFreshForm(self.freshFormInfo))
		myelDiagView.myelomaDiagnosisSavedForm.continue_button.click()


		# Should have first 3 questions + 8 default questions
		formInfo = {
			'questions': self.currentQuestions + self.defaultQuestions,
			'meta': [{'num_questions': 8}],
		}
		# Bug: Doesn't display 3 currentQuestions
		self.assertTrue(currentHealthView.on(formInfo))
		self.driver.refresh()
		self.assertTrue(currentHealthView.on())
		self.assertNotEquals(currentHealthView.menu.selected_option(), 'Current Health')
		raw_input('how many questions?')
		self.assertTrue(currentHealthView.submit(formInfo))

		# Delete Diagnosis
		self.assertTrue(fitLvlView.on())
		fitLvlView.menu.go_to('Myeloma Diagnosis')
		self.assertTrue(myelDiagView.on('saved'))
		myelDiagView.delete('diagnosis', 0)

	def test_recent_diagnosis(self):
		'''CurrentHealth : CurrentHealth . test_non_recent_diagnosis'''
		# Andrew: Go to 'Myeloma Diagnosis' and save diagnosis that is recent
		# Continue on to 'Current Health' and verify form only has 8 questions

		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		currentHealthView = self.andrew.currentHealthView
		fitLvlView = self.andrew.fitLvlView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())
		aboutMeView.menu.go_to('Myeloma Diagnosis')

		# Submit recent Diagnosis
		self.assertTrue(myelDiagView.on('fresh'))
		freshFormInfo = copy.deepcopy(self.freshFormInfo)
		# freshFormInfo['newly_diagnosed'] = 'yes'
		self.assertTrue(myelDiagView.submitFreshForm(freshFormInfo))
		myelDiagView.myelomaDiagnosisSavedForm.continue_button.click()

		# Should have 8 default questions
		formInfo = {
			'questions': self.defaultQuestions,
			'meta': [{'num_questions': 8}],
		}
		self.assertTrue(currentHealthView.on(formInfo))
		self.assertTrue(currentHealthView.submit(formInfo))

		# Delete Diagnosis
		self.assertTrue(fitLvlView.on())
		fitLvlView.menu.go_to('Myeloma Diagnosis')
		self.assertTrue(myelDiagView.on('saved'))
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
			'questions': self.currentQuestions + self.defaultQuestions,
			'meta': [{'num_questions': 8}],
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
			'questions': self.currentQuestions + updatedQuestions,
			'meta': [{'num_questions': 8}],
		}
		currentHealthView.currentHealthForm.answer_question(3, heartConditions)
		currentHealthView.currentHealthForm.answer_question(4, lungConditions)
		currentHealthView.currentHealthForm.answer_question(5, kidneyConditions)
		self.assertTrue(currentHealthView.on(updatedFormInfo))

		# Reset to default answers (I don't know)
		self.assertTrue(currentHealthView.submit(defaultFormInfo))

	def test_additional_questions(self):
		'''CurrentHealth : CurrentHealth . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelDiagView = self.andrew.myelomaDiagnosisView
		fitLvlView = self.andrew.fitLvlView
		currentHealthView = self.andrew.currentHealthView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Diagnosis')
		self.assertTrue(myelDiagView.on('fresh'))

		freshFormInfo = copy.deepcopy(self.freshFormInfo)
		freshFormInfo['type'] = 'smoldering myeloma'
		self.assertTrue(myelDiagView.submitFreshForm(freshFormInfo))
		myelDiagView.myelomaDiagnosisSavedForm.continue_button.click()

		formInfo = {
			'questions': self.defaultQuestions,
			'meta': [{'num_questions': 8}],
		}
		self.assertTrue(currentHealthView.on(formInfo))
		self.assertTrue(currentHealthView.submit(formInfo))

		# Delete Diagnosis
		self.assertTrue(fitLvlView.on())
		fitLvlView.menu.go_to('Myeloma Diagnosis')
		self.assertTrue(myelDiagView.on('saved'))
		myelDiagView.delete('diagnosis', 0)




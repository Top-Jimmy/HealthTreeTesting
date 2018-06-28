import unittest
import main
import initDriver
import profiles
import form_info
# import copy # copy.deepcopy(object)

# @unittest.skip("In progress")
class TestAddTreatment(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

		# single question
		self.question_template = {
			'type': 'single',
			'options': [
				{'Chemotherapy/Myeloma Therapy': {} } # key = text of label for radio option
			],
		}

		# single question w/ comment
		self.question_template = {
			'type': 'single',
			'options': [
				{'Chemotherapy/Myeloma Therapy': {'comment': 'Comment text'} }
			],
		}

		# single question w/ secondaryQuestions
		self.question_template = {
			'type': 'single',
			'options': [
				{'I discontinued this treatment': {
						'type': 'select-all',
						'options': [
							{'Cost of the treatment': {} },
							{'Too much travel': {} },
							{'Other': {'comment': 'Comment text', 'actions': 'continue', } }
						]
					},
				}
			],
		}

		# select-all question w/ no subquestions or comments
		self.question_template = {
			'type': 'select-all',
			'options': [
				{'Option X': {} },
				{'Option Y': {} },
				{'Option Z': {} },
			],
		}

		# date question
		self.question_template = {
			'type': 'date',
			'text': '10/5',
		}

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		'''AddTreatment : AddTreatment . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())

	def test_add_radiation(self):
		'''AddTreatment : AddTreatment . test_add_radiation'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())

		treatment1 = {
			'questions': [
				{'type': 'single',
					'options': {
						'Radiation': {},
					},
				},
				{'type': 'single',
					'options': {
						'Other': {'comment': 'Type of Radiation: Treatment1'},
					},
					'actions': 'continue',
				},
				{'type': 'date', 'text': '10/2017' },
				{'type': 'date', 'text': '02/2018' },
				{'type': 'single',
					'options': {
						'I discontinued this treatment': {
							'type': 'select-all',
							'options': {
								'Cost of the treatment': {},
								'Too much travel': {},
								'Other': {'comment': 'Comment text'},
							},
						}
					},
					'actions': 'continue',
				},
			],
			# 'sideEffects': form_info.get_info('sideEffects'),
			'sideEffects': {
				'cardiovascular/circulatory system': {
    			'blood clots': 9,
    			'irregular/rapid heartbeat': 2,
    		}
    	}
		}
		self.assertTrue(toView.add_treatment(treatment1, 'save'))

		treatment2 = {
			'questions': [
				{'name': 'Radiation'

				}
			]
		}

		treatment2 = {
			'questions': [
				{'type': 'single',
					'name': 'What was the type of myeloma treatment you received?',
					'options': {
						'Radiation': {},
					},
				},
				{'type': 'single',
					'name': 'What type of Radiation treatment did you receive?',
					'options': {
						'Local Radiation': {},
					},
					'actions': 'continue',
				},
				{'type': 'date', 'text': '10/2015' },
				{'type': 'date', 'text': '02/2016' },
				{'type': 'single',
					'options': {
						'I discontinued this treatment': {
							'type': 'select-all',
							'options': {
								'Too much travel': {},
								'Other': {'comment': 'Discontinued comment: Treatment2'},
							},
						}
					},
					'actions': 'continue',
				},
			],
			'sideEffects': {
				'cardiovascular/circulatory system': {
    			'low potassium': 2,
    			'low blood pressure': 5,
    		}
    	}
		}
		self.assertTrue(toView.add_treatment(treatment2, 'save'))

		raw_input('what order?')

		# expectedValues = {
		# 	'tests': [treatment1, treatment2],
		# }
		# self.assertTrue(toView.on())















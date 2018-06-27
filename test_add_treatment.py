import unittest
import main
import initDriver
import profiles
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

		treatmentInfo = [
			{'type': 'single',
				'options': {
					'Radiation': {},
				},
			},
			{'type': 'single',
				'options': {
					'Other': {'comment': 'Bogus'},
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
						'actions': 'continue',
					}
				},
			},
		]
		toView.add_treatment(treatmentInfo, 'wait')


		raw_input('?')













import unittest
import main
import initDriver
import profiles
import form_info
# import copy # copy.deepcopy(object)

# single question
# self.question_template = {
# 	'type': 'single',
# 	'options': [
# 		{'Chemotherapy/Myeloma Therapy': {} } # key = text of label for radio option
# 	],
# }

# # single question w/ comment
# self.question_template = {
# 	'type': 'single',
# 	'options': [
# 		{'Chemotherapy/Myeloma Therapy': {'comment': 'Comment text'} }
# 	],
# }

# # single question w/ secondaryQuestions
# self.question_template = {
# 	'type': 'single',
# 	'options': [
# 		{'I discontinued this treatment': {
# 				'type': 'select-all',
# 				'options': [
# 					{'Cost of the treatment': {} },
# 					{'Too much travel': {} },
# 					{'Other': {'comment': 'Comment text', 'actions': 'continue', } }
# 				]
# 			},
# 		}
# 	],
# }

# # select-all question w/ no subquestions or comments
# self.question_template = {
# 	'type': 'select-all',
# 	'options': {
# 		'Option X': {},
# 		'Option Y': {},
# 		'Option Z': {},
# 	},
# }

# # date question
# self.question_template = {
# 	'type': 'date',
# 	'text': '10/5',
# }

class TestChemotherapy(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_chemotherapy(self):
	'''AddTreatment : TestChemotherapy . test_chemotherapy'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())

		# Chemo: Currently taking
		# Should have 8 questions (base amount)
		treatment1 = {
			'questions': [
				{'type': 'single',	# Treatment Type
					'options': {
						'Chemotherapy/Myeloma Therapy': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # Start date
				{'type': 'single',	# Currently taking?
					'options': {
						'Yes': {},
					},
				},
				{'type': 'single',	# Maintenance therapy? (don't think it matters how you answer this question)
					'options': {
						'Yes': {},
					},
				},
				{'type': 'complex', # Chemo treatment options
					'options': {
						'chemotherapies': {
		    			'Melphalan': None,
		    			'Adriamycin': None,
		    		}
		    		'clinical trial drugs or other': {
		    			'venclexta (venetoclax)': None,
		    			'Other': {'comment': 'Chemo Treatment X'},
		    		}
		    	}
				},
				{'type': 'single',	# Changes to treatment?
					'options': {
						'No': {},
					},
				},
				{'type': ,	# Best response?
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'complex', # Side effects
					'options': {
						'cardiovascular/circulatory system': {
		    			'blood clots': 9,
		    			'irregular/rapid heartbeat': 2,
		    		}
		    	}
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment1, 'save'))

		# Chemo: Stopped taking
		# Should have 9 questions (+1 for stop date)
		treatment2 = {
			'questions': [
				{'type': 'single',	# Treatment Type
					'options': {
						'Chemotherapy/Myeloma Therapy': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # Start date
				{'type': 'single',	# Currently taking?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 'text': '/2018' }, # Stop date
				{'type': 'single',	# Maintenance therapy? (don't think it matters how you answer this question)
					'options': {
						'Yes': {},
					},
				},
				{'type': 'complex', # Chemo treatment options
					'options': {
						'chemotherapies': {
		    			'Melphalan': None,
		    			'Adriamycin': None,
		    		}
		    		'clinical trial drugs or other': {
		    			'venclexta (venetoclax)': None,
		    			'Other': {'comment': 'Chemo Treatment X'},
		    		}
		    	}
				},
				{'type': 'single',	# Changes to treatment?
					'options': {
						'No': {},
					},
				},
				{'type': ,	# Best response?
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'complex', # Side effects
					'options': {
						'cardiovascular/circulatory system': {
		    			'blood clots': 9,
		    			'irregular/rapid heartbeat': 2,
		    		}
		    	}
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment2, 'save'))


class TestRadiation(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_add_radiation(self):
		'''AddTreatment : TestRadiation . test_add_radiation'''
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
						'Other': {'comment': 'Radiation treatment X'},
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
								'Other': {'comment': 'Discontinued because Y'},
							},
						}
					},
					'actions': 'continue',
				},
			],
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

		# Reset: Delete treatments
		self.assertTrue(toView.add_treatment(treatment2, 'save'))
		toView.edit(1, 'delete', {'meta': {'num_treatments': 1}})
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})


class TestExtra(unittest.TestCase):
	# Tests treatments for: Bone strengtheners, antibiotics, antifungals

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_bone_strengthener(self):
		'''AddTreatment : TestExtra . test_bone_strengthener'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		# Not currently taking bone strengtheners
		treatment1 = {
			'questions': [
				{'type': 'single',
					# Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',
					# Supportive Care Type
					'options': {
						'Bone Strengthener': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',
					# Bone strengthener Type
					'options': {
						'Aredia': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # Start date
				{'type': 'single',
					# Bone Strengtheners: Same Frequency
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 'text': '02/2018' }, # Stop date
				{'type': 'single',
					# Bone Strengtheners: Frequency
					'options': {
						'Yearly': {},
					},
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment1, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

		# Currently taking bone strengtheners
		treatment2 = {
			'questions': [
				{'type': 'single',
					# Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',
					# Supportive Care Type
					'options': {
						'Bone Strengthener': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',
					# Bone strengthener Type
					'options': {
						'Denosumab': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # Start date
				{'type': 'single',
					# Bone Strengtheners: Same Frequency
					'options': {
						'No': {},
					},
				},
				{'type': 'single',
					# Bone Strengtheners: Frequency
					'options': {
						'Once every 3 months': {},
					},
				},
			]
		}

	def test_antibiotics(self):
		'''AddTreatment : TestExtra . test_antibiotics'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		# Not currently taking antibiotics
		treatment1 = {
			'questions': [
				{'type': 'single',
					# Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',
					# Supportive Care Type
					'options': {
						'Antibiotics': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',
					# Antibiotics Type
					'options': {
						'Biaxin (clarithromycin)': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # Start date
				{'type': 'single',
					# Still taking antibiotics?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 'text': '02/2018' }, # Stop date
			]
		}
		self.assertTrue(toView.add_treatment(treatment1, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

		# Still taking antibiotics
		treatment2 = {
			'questions': [
				{'type': 'single',
					# Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',
					# Supportive Care Type
					'options': {
						'Antibiotics': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',
					# Antibiotics Type
					'options': {
						'Biaxin (clarithromycin)': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # Start date
				{'type': 'single',
					# Still taking antibiotics?
					'options': {
						'Yes': {},
					},
				}
			]
		}
		self.assertTrue(toView.add_treatment(treatment2, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

	def test_antifungal(self):
		'''AddTreatment : TestExtra . test_antifungal'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		# Not currently taking antibiotics
		treatment1 = {
			'questions': [
				{'type': 'single',
					# Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',
					# Supportive Care Type
					'options': {
						'Anti-Fungal': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',
					# Anti-fungal Type
					'options': {
						'Amphotericin B': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # Start date
				{'type': 'single',
					# Still taking antifungals?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 'text': '02/2018' }, # Stop date
			]
		}
		self.assertTrue(toView.add_treatment(treatment1, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

		# Still taking antibiotics
		treatment2 = {
			'questions': [
				{'type': 'single',
					# Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',
					# Supportive Care Type
					'options': {
						'Anti-Fungal': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',
					# Anti-fungal Type
					'options': {
						'Amphotericin B': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # Start date
				{'type': 'single',
					# Still taking antifungals?
					'options': {
						'Yes': {},
					},
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment2, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})


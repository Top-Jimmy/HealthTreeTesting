import unittest
import main
import initDriver
import profiles
import form_info
# import copy # copy.deepcopy(object)

class TestChemotherapy(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_current_chemotherapy(self):
		'''AddTreatment : TestChemotherapy . test_chemotherapy'''
		# Different flows depending on how you answer question #3 (Are you currently taking chemotherapy)
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
		    		},
		    		'clinical trial drugs or other': {
		    			'venclexta (venetoclax)': None,
		    			'Other': {'comment': 'Chemo Treatment X'},
		    		},
		    	}
				},
				{'type': 'single',	# Changes to treatment?
					'options': {
						'No': {},
					},
				},
				{'type': 'single',	# Best response?
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'complex', # Side effects
					'options': {
						'cardiovascular/circulatory system': {
		    			'blood clots': {'intensity': 9},
		    			'irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment1))

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
				{'type': 'date', 'text': '02/2018' }, # Stop date
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
		    		},
		    		'clinical trial drugs or other': {
		    			'venclexta (venetoclax)': None,
		    			'Other': {'comment': 'Chemo Treatment X'},
		    		},
		    	}
				},
				{'type': 'single',	# Changes to treatment?
					'options': {
						'No': {},
					},
				},
				{'type': 'single',	# Best response?
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'complex', # Side effects
					'options': {
						'cardiovascular/circulatory system': {
		    			'blood clots': {'intensity': 9},
		    			'irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment2))

		toView.edit(1, 'delete', {'meta': {'num_treatments': 1}})
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

	def test_changed_chemotherapy(self):
		'''AddTreatment : TestChemotherapy . test_chemotherapy'''
		# Different flows depending on whether medications were added/removed during treatment
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())

		# Chemo: Medications were added and removed
		# Should have 10 questions: 8 (base amount) +1 (added) +1 (removed)
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
		    			'Adriamycin': None,
		    		},
		    		'steroids': {
		    			'Dexamethasone': None,
		    		},
		    	}
				},
				{'type': 'single',	# Changes to treatment?
					'options': {
						'Yes': {
							'type': 'select-all',
							'options': {
								'Yes, my doctor added some medications to my treatment': {},
								'Yes, my doctor removed some medications from my treatment': {},
							},
						}
					},
					'actions': 'continue',
				},
				{'type': 'complex', # Drugs ADDED
					'date': '12/2017',
					'options': {
						'chemotherapies': {'melphalan': None,}
					}
				},
				{'type': 'table', # Drugs REMOVED
					'options': {
						'dexamethasone': {
		    			'date stopped': '03/2018',
		    			'reason stopped': 'too much travel',
		    		},
		    		'adriamycin': {
		    			'date stopped': '03/2018',
		    			'reason stopped': 'drug cost',
		    		},
		    		'melphalan': {},
		    	}
				},
				{'type': 'single',	# Best response?
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'complex', # Side effects
					'options': {
						'cardiovascular/circulatory system': {
		    			'blood clots': {'intensity': 9},
		    			'irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment1))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

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
				{'type': 'complex', # Side effects
					'options': {
						'cardiovascular/circulatory system': {
		    			'blood clots': {'intensity': 9},
		    			'irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			],
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
				{'type': 'complex', # Side effects
					'options': {
						'cardiovascular/circulatory system': {
		    			'low potassium': {'intensity': 2},
		    			'low blood pressure': {'intensity': 5},
		    		}
		    	}
				},
			],
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
					'actions': 'continue',
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
		self.assertTrue(toView.add_treatment(treatment2, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

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


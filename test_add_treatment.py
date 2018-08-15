import unittest
import main
import initDriver
import profiles
import form_info
# import copy # copy.deepcopy(object)

# TestChemotherapy
#   test_changed_chemotherapy
# 	test_current_chemotherapy					Edit treatments, outcomes (side effects)
# TestClinical
#   test_clinical_basic								Edit treatment (#866), outcomes (side effects)
# TestRadiation
# 	test_add_radiation
# TestExtra
# 	test_bone_strengthener: 					Question[4] still taking bone strengtheners?
# 	test_antibiotics: 								Question[4] Still taking antibiotics?
# 	test_antifungal: 									Question[4] still taking antifungal?
# TestStemCell
# 	test_basic
@unittest.skip('Dont need to run these')
class TestChemotherapy(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_changed_chemotherapy(self):
		''' test_add_treatment.py:TestChemotherapy.test_changed_chemotherapy '''
		# Different flows depending on whether medications were added/removed during treatment
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		toView.delete_all_treatments()

		# Chemo: Medications were added and removed
		# Should have 10 questions: 8 (base amount) +1 (added) +1 (removed)
		treatment1 = {
			'testMeta': {'type': 'chemo'},
			'questions': [
				{'type': 'single',	# 0: Treatment Type
					'options': {
						'Chemotherapy/Myeloma Therapy': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # 1: Start date
				{'type': 'single',	# 2: Currently taking?
					'options': {
						'Yes': {},
					},
				},
				{'type': 'single',	# 3: Maintenance therapy? (don't think it matters how you answer this question)
					'options': {
						'Yes': {},
					},
				},
				{'type': 'popup', # 4: Chemo treatment options
					'options': {
						'Chemotherapies': {
		    			'Adriamycin': None,
		    		},
		    		'Steroids': {
		    			'Dexamethasone': None,
		    		},
		    	}
				},
				{'type': 'single',	# 5: Changes to treatment?
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
				{'type': 'complex', # 6: Drugs ADDED
					'date': '12/2017',
					'options': {
						'Chemotherapies': {'Melphalan': None}
					}
				},
				{'type': 'table', # 7: Drugs REMOVED
					'options': {
						'Dexamethasone': {
		    			'date stopped': '03/2018',
		    			'reason stopped': 'Too much travel',
		    		},
		    		'Adriamycin': {
		    			'date stopped': '03/2018',
		    			'reason stopped': 'Drug cost',
		    		},
		    		'Melphalan': {},
		    	}
				},
				{'type': 'single',	# 8: Best response?
					'options': {
						'The treatment initially reduced my myeloma but my myeloma began to increase and required a treatment change': {},
					},
				},
				{'type': 'popup', # 9: Side effects
					'options': {
						'Cardiovascular/Circulatory System': {
		    			'Blood clots': {'intensity': 9},
		    			'Irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment1))
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

	def test_current_chemotherapy(self):
		''' test_add_treatment.py:TestChemotherapy.test_current_chemotherapy '''
		# Different flows depending on how you answer question[2] (Are you currently taking chemotherapy)
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		toView.delete_all_treatments()

		# Chemo: Currently taking
		# Should have 8 questions (base amount)
		treatment1 = {
			'testMeta': {'type': 'chemo'},
			'questions': [
				{'type': 'single',	# 0: Treatment Type
					'options': {
						'Chemotherapy/Myeloma Therapy': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # 1: Start date
				{'type': 'single',	# 2: Currently taking?
					'options': {
						'Yes': {},
					},
				},
				{'type': 'single',	# 3: Maintenance therapy? (don't think it matters how you answer this question)
					'options': {
						'Yes': {},
					},
				},
				{'type': 'popup', # 4: Chemo treatment options
					'options': {
						'Chemotherapies': {
		    			'Melphalan': None,
		    			'Adriamycin': None,
		    		},
		    		'Proteasome Inhibitors': {
		    			'Kyprolis (carfilzomib)': None,
		    		},
		    	}
				},
				{'type': 'single',	# 5: Changes to treatment?
					'options': {
						'No': {},
					},
				},
				{'type': 'single',	# 6: Best response?
					'options': {
						'I am currently on this treatment and my response is unknown': {},
					},
				},
				{'type': 'popup', # 7: Side effects
					'options': {
						'Cardiovascular/Circulatory System': {
		    			'Blood clots': {'intensity': 9},
		    			'Irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment1))

		editValues = [
			{'num_questions': 9},
			{'index': 1, 'date': '11/2016'},
			{'index': 2, 'options': {
				'No': {},
			}},
			{'index': 3, 'date': '03/2018'},
			{'index': 5, 'complex': {
				'Chemotherapies': {
    			'Melphalan': {},
    			'D-PACE': {},
    		},
    		'Proteasome Inhibitors': {
    			'Ninlaro (ixazomib)': {},
    		},
			}},
			{'index': -1, 'complex': {
				'Cardiovascular/Circulatory System': {
    			'Blood clots': {'intensity': 7},
    			'Irregular/rapid heartbeat': {'intensity': 5},
    		}
			}},
		]
		treatment1Edited = {
			'testMeta': {'type': 'chemo'},
			'questions': [
				{'type': 'single',	# 0: Treatment Type
					'options': {
						'Chemotherapy/Myeloma Therapy': {},
					},
				},
				{'type': 'date', 'text': '11/2016' }, # 1: Start date
				{'type': 'single',										# 2: Currently taking?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 'text': '03/2018' }, # 3: Start date
				{'type': 'single',	# 4: Maintenance therapy? (don't think it matters how you answer this question)
					'options': {
						'Yes': {},
					},
				},
				{'type': 'popup', # 5: Chemo treatment options
					'options': {
						'Chemotherapies': {
		    			'Melphalan': None,
		    			'D-PACE': None,
		    		},
		    		'Proteasome Inhibitors': {
		    			'Ninlaro (ixazomib)': None,
		    		},
		    	}
				},
				{'type': 'single',	# 6: Changes to treatment?
					'options': {
						'No': {},
					},
				},
				{'type': 'single',	# 7: Best response?
					'options': {
						'I am currently on this treatment and my response is unknown': {},
					},
				},
				{'type': 'popup', # 8: Side effects
					'options': {
						'Cardiovascular/Circulatory System': {
		    			'Blood clots': {'intensity': 7},
		    			'Irregular/rapid heartbeat': {'intensity': 5},
		    		}
		    	}
				},
			]
		}
		# Edit Treatment
		toView.edit_treatment(0, 'treatments', treatment1Edited, editValues)

		# Edit Outcome
		new_outcome = {'The treatment did not reduce my myeloma': {}}
		treatment1Edited['questions'][7]['options'] = new_outcome
		toView.edit_treatment(0, 'outcomes', treatment1Edited, new_outcome)

		# Edit Side Effects
		new_effects = {
			'Other': {
  			'Infusion related reactions': {'intensity': 5},
  			'Insomnia': {'intensity': 6},
  			'Tremors': {'intensity': 4},
  		}
		}
		treatment1Edited['questions'][-1]['options'] = new_effects
		toView.edit_treatment(0, 'side effects', treatment1Edited, new_effects)

		# Chemo: Stopped taking
		# Should have 9 questions (+1 for stop date)
		treatment2 = {
			'testMeta': {'type': 'chemo'},
			'questions': [
				{'type': 'single',	# 0: Treatment Type
					'options': {
						'Chemotherapy/Myeloma Therapy': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # 1: Start date
				{'type': 'single',	# 2: Currently taking?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 'text': '02/2018' }, # 3: Stop date
				{'type': 'single',	# 4: Maintenance therapy? (don't think it matters how you answer this question)
					'options': {
						'No': {},
					},
				},
				{'type': 'popup', # 5: Chemo treatment options
					'options': {
						'Chemotherapies': {
		    			'Melphalan': None,
		    			'Adriamycin': None,
		    		},
		    		'Proteasome Inhibitors': {
		    			'Kyprolis (carfilzomib)': None,
		    		},
		    	}
				},
				{'type': 'single',	# 6: Changes to treatment?
					'options': {
						'No': {},
					},
				},
				{'type': 'single',	# 7: Best response?
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'popup', # 8: Side effects
					'options': {
						'Cardiovascular/Circulatory System': {
		    			'Blood clots': {'intensity': 9},
		    			'Irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			]
		}
		# Most recent tests should be first
		self.assertTrue(toView.add_treatment(treatment2, [treatment2, treatment1Edited]))

		toView.edit_treatment(1, 'delete', {'meta': {'num_treatments': 1}})
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

@unittest.skip('Dont need to run these')
class TestClinical(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_clinical_basic(self):
		''' test_add_treatment.py:TestClinical.test_clinical_basic '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		toView.delete_all_treatments()

		# Not on trial anymore
		treatment1 = {
			'testMeta': {'type': 'clinical'},
			'questions': [
				{'type': 'single', 		# 0: Treatment Type
					'options': {
						'Clinical Trials': {},
					},
				},
				{'type': 'input', 		# 1: NCT number
					'text': 'NCT00000419',
					'actions': 'continue',
				},
				{'type': 'date', 'text': '10/2017' },	# 2: Start Date
				{'type': 'single',										# 3: Still on trial?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 'text': '02/2018' }, # 4: Stop Date
				{'type': 'input', 										# 5: Main treatment
					'text': 'Test Treatment',
					'actions': 'continue',
				},
				{'type': 'single',										# 6: Best response?
					'options': {
						'I discontinued this treatment': {
							'type': 'select-all',
							'options': {
								'Severity of the side effects': {},
								'Cost of the treatment': {},
								'Other': {'comment': 'Discontinued because Y'},
							},
						}
					},
					'actions': 'continue',
				},
				{'type': 'popup', 								# 7: Side effects
					'options': {
						'Cardiovascular/Circulatory System': {
		    			'Blood clots': {'intensity': 9},
		    			'Irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			],
		}
		self.assertTrue(toView.add_treatment(treatment1))
		# raw_input('added 1')
		editValues = [
			{'num_questions': 8},
			{'index': 1, 'date': '10/2015'},
			{'index': 3, 'date': '03/2017'},
			{'index': 4, 'text': 'NCT00000421'},
	    {'index': 5, 'text': 'Test Treatment X'},
	    {'index': -1, 'complex': {
				'Lymphatic/Immune System': {
	    		'Fatigue/tired': {'intensity': 5},
	    		'Mouth sores': {'intensity': 4},
    		}
	    }},
		]
		treatment1Edited = {
			'testMeta': {'type': 'clinical'},
			'questions': [
				{'type': 'single', 		# 0: Treatment Type
					'options': {
						'Clinical Trials': {},
					},
				},
				{'type': 'input', 		# 1: NCT number
					'text': 'NCT00000421',
					'actions': 'continue',
				},
				{'type': 'date', 'text': '10/2015' },	# 2: Start Date
				{'type': 'single',										# 3: Still on trial?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 'text': '03/2017' }, # 4: Stop Date
				{'type': 'input', 										# 5: Main treatment
					'text': 'Test Treatment X',
					'actions': 'continue',
				},
				{'type': 'single',										# 6: Best response?
					'options': {
						'I discontinued this treatment': {
							'type': 'select-all',
							'options': {
								'Severity of the side effects': {},
								'Cost of the treatment': {},
								'Other': {'comment': 'Discontinued because Y'},
							},
						}
					},
				},
				{'type': 'popup', 								# 7: Side effects
					'options': {
						'Lymphatic/Immune System': {
			    		'Fatigue/tired': {'intensity': 5},
			    		'Mouth sores': {'intensity': 4},
		    		}
		    	}
				},
			],
		}
		toView.edit_treatment(0, 'treatments', treatment1Edited, editValues)

		new_outcome = {'My myeloma is now undetectable': {
			'type': 'single',
			'options': {
				'I dont know the details of my response': {},
			},
		}}
		# Edit Outcomes
		edited_outcome = {'options': new_outcome}
		treatment1Edited['questions'][-2]['options'] = new_outcome
		toView.edit_treatment(0, 'outcomes', treatment1Edited, edited_outcome)

		# Edit Side Effects
		new_effects = {
			'Renal/Urinary System': {
  			'Kidney damage': {'intensity': 3},
  			'Kidney failure': {'intensity': 4},
  			'Liver failure': {'intensity': 5},
  		}
		}
		treatment1Edited['questions'][-1]['options'] = new_effects
		toView.edit_treatment(0, 'side effects', treatment1Edited, new_effects)
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

		# Still on trial
		treatment2 = {
			'testMeta': {'type': 'clinical'},
			'questions': [
				{'type': 'single', 		# 0: Treatment Type
					'options': {
						'Clinical Trials': {},
					},
				},
				{'type': 'input', 		# 1: NCT number
					'text': 'NCT00000419',
					'actions': 'continue',
				},
				{'type': 'date', 'text': '10/2017' },	# 2: Start Date
				{'type': 'single',										# 3: Still on trial?
					'options': {
						'Yes': {},
					},
				},
				{'type': 'input', 										# 4: Main treatment
					'text': 'Test Treatment',
					'actions': 'continue',
				},
				{'type': 'single',										# 5: Best response?
					'options': {
						'My myeloma is now undetectable': {
							'type': 'single',
							'options': {
								'I had a complete response (CR) to the treatment': {},
							},
						},
					},
				},
				{'type': 'popup', 								# 6: Side effects
					'options': {
						'Cardiovascular/Circulatory System': {
		    			'Blood clots': {'intensity': 9},
		    			'Irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			],
		}
		# self.assertTrue(toView.on({'tests': [treatment1]}))
		self.assertTrue(toView.add_treatment(treatment2))
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

@unittest.skip('wont pass')
class TestRadiation(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_add_radiation(self):
		''' test_add_treatment.py:TestRadiation.test_add_radiation '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		toView.delete_all_treatments()

		radiation1 = {
			'testMeta': {'type': 'radiation'},
			'questions': [
				{'type': 'single', 		# 0: Treatment Type
					'options': {
						'Radiation': {},
					},
				},
				{'type': 'single', 		# 1: Radiation Type
					'options': {
						'Other': {'comment': 'Radiation treatment X'},
					},
					'actions': 'continue',
				},
				{'type': 'date', 'text': '10/2017' },	# 2: Start Date
				{'type': 'date', 'text': '02/2018' }, # 3: Stop Date
				{'type': 'single',										# 4: Best Response
					'options': {
						'I discontinued this treatment': {
							'type': 'select-all',
							'options': {
								'Severity of the side effects': {},
								'Cost of the treatment': {},
								'Other': {'comment': 'Discontinued because Y'},
							},
						}
					},
					'actions': 'continue',
				},
				{'type': 'popup', 								# 5: Side effects
					'options': {
						'Cardiovascular/Circulatory System': {
		    			'Blood clots': {'intensity': 9},
		    			'Irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			],
		}
		self.assertTrue(toView.add_treatment(radiation1))

		editValues = [
			{'num_questions': 6},
			{'index': 1, 'options': {
					'Other': {'comment': 'Radiation treatment Y'},
				},
			},
			{'index': 2, 'date': '08/2017'},
			{'index': 3, 'date': '01/2018'},
			{'index': -2, 'options': {
				'I discontinued this treatment': {
					'select-all': {
						'Too much travel': {},
						'Too much time in the clinic': {},
					},
				}
			}},
			{'index': -1, 'complex': {
				'Cardiovascular/Circulatory System': {
    			'Low blood pressure': {'intensity': 7},
    			'Low potassium': {'intensity': 5},
    		}
	    }},
		]
		radiation1Edited = {
			'testMeta': {'type': 'radiation'},
			'questions': [
				{'type': 'single', 		# 0: Treatment Type
					'options': {
						'Radiation': {},
					},
				},
				{'type': 'single', 		# 1: Radiation Type
					'options': {
						'Other': {'comment': 'Radiation treatment Y'},
					},
					'actions': 'continue',
				},
				{'type': 'date', 'text': '08/2017' },	# 2: Start Date
				{'type': 'date', 'text': '01/2018' }, # 3: Stop Date
				{'type': 'single',										# 4: Best Response
					'options': {
						'I discontinued this treatment': {
							'type': 'select-all',
							'options': {
								'Too much travel': {},
								'Too much time in the clinic': {},
							},
						}
					},
					'actions': 'continue',
				},
				{'type': 'popup', 								# 5: Side effects
					'options': {
						'Cardiovascular/Circulatory System': {
		    			'low blood pressure': {'intensity': 7},
		    			'low potassium': {'intensity': 5},
		    		}
		    	}
				},
			],
		}
		toView.edit_treatment(0, 'treatments', radiation1Edited, editValues)

		new_outcome = {'My myeloma is now undetectable': {
			'options': {
				'I dont know the details of my response': {},
			}
		}}
		edited_outcome = {'options': new_outcome}
		radiation1Edited['questions'][4]['options'] = new_outcome
		toView.edit_treatment(0, 'outcomes', radiation1Edited, edited_outcome)

		radiation2 = {
			'testMeta': {'type': 'radiation'},
			'questions': [
				{'type': 'single',											# 0: Treatment Type
					'name': 'What was the type of myeloma treatment you received?',
					'options': {
						'Radiation': {},
					},
				},
				{'type': 'single',											# 1: Radiation Type
					'name': 'What type of Radiation treatment did you receive?',
					'options': {
						'Local Radiation': {},
					},
				},
				{'type': 'date', 'text': '10/2015' },		# 2: Start Date
				{'type': 'date', 'text': '02/2016' },		# 3: End Date
				{'type': 'single',											# 4: Best Response
					'options': {
						'I discontinued this treatment': {
							'type': 'select-all',
							'options': {
								'Too much travel': {},
								'Too much time in the clinic': {},
								'Other': {'comment': 'Discontinued comment: Treatment2'},
							},
						}
					},
					'actions': 'continue',
				},
				{'type': 'popup', 										# 5: Side effects
					'options': {
						'Cardiovascular/Circulatory System': {
		    			'low potassium': {'intensity': 2},
		    			'low blood pressure': {'intensity': 5},
		    		}
		    	}
				},
			],
		}

		# Reset: Delete treatments
		self.assertTrue(toView.add_treatment(radiation2))
		toView.delete_all_treatments()
		
@unittest.skip('wont pass')
class TestExtra(unittest.TestCase):
	# Tests treatments for: Bone strengtheners, antibiotics, antifungals

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_bone_strengthener(self):
		''' test_add_treatment.py:TestExtra.test_bone_strengthener '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		toView.delete_all_treatments()

		# Not currently taking bone strengtheners
		treatment1 = {
			'testMeta': {'type': 'bone strengtheners'},
			'questions': [
				{'type': 'single', 			# 0: Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single', 			# 1. Supportive Care Type
					'options': {
						'Bone Strengthener': {},
					},
					'actions': 'continue',
				},
				{'type': 'single', 			# 2. Bone strengthener Type
					'options': {
						'Aredia': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # 3. Start date
				{'type': 'single',										# 4. Bone Strengtheners: Same Frequency
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 'text': '02/2018' }, # 5. Stop date
				{'type': 'single', 										# 6. Bone Strengtheners: Frequency
					'options': {
						'Yearly': {},
					},
					'actions': 'continue',
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment1))

		editValues = [
			{'num_questions': 6},
			{'index': 1, 'options': 'Zometa'},
			{'index': 2, 'date': '11/2017'},
			{'index': 4, 'date': '03/2018'},
			{'index': 5, 'options': 'Once every 6 months'},
		]
		treatment1Edited = {
			'testMeta': {'type': 'bone strengtheners'},
			'questions': [
				{'type': 'single', 			# 0: Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single', 			# 1. Supportive Care Type
					'options': {
						'Bone Strengthener': {},
					},
					'actions': 'continue',
				},
				{'type': 'single', 			# 2. Bone strengthener Type
					'options': {
						'Zometa': {},
					},
				},
				{'type': 'date', 'text': '11/2017' }, # 3. Start date
				{'type': 'single',										# 4. Bone Strengtheners: Same Frequency
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 'text': '03/2018' }, # 5. Stop date
				{'type': 'single', 										# 6. Bone Strengtheners: Frequency
					'options': {
						'Once every 6 months': {},
					},
					'actions': 'continue',
				},
			]
		}
		toView.edit_treatment(0, 'treatments', treatment1Edited, editValues)
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

		# Currently taking bone strengtheners
		treatment2 = {
			'testMeta': {'type': 'bone strengtheners'},
			'questions': [
				{'type': 'single',					# 0. Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',					# 1. Supportive Care Type
					'options': {
						'Bone Strengthener': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',					# 2. Bone strengthener Type
					'options': {
						'Denosumab': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # 3. Start date
				{'type': 'single',										# 4. Bone Strengtheners: Same Frequency
					'options': {
						'Yes': {},
					},
				},
				{'type': 'single',										# 5. Bone Strengtheners: Frequency
					'options': {
						'Once every 3 months': {},
					},
					'actions': 'continue',
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment2))
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

	def test_antibiotics(self):
		''' test_add_treatment.py:TestExtra.test_antibiotics '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		toView.delete_all_treatments()

		# Not currently taking antibiotics
		treatment1 = {
			'testMeta': {'type': 'antibiotics'},
			'questions': [
				{'type': 'single', 									# 0. Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',									# 1. Supportive Care Type
					'options': {
						'Antibiotics': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',									# 2. Antibiotics Type
					'options': {
						'Biaxin (clarithromycin)': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # 3. Start date
				{'type': 'single', 										# 4. Still taking antibiotics?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 											# 5. Stop date
					'text': '02/2018',
					'actions': 'continue',
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment1))

		editValues = [
			{'num_questions': 5},
			{'index': 1, 'options': 'Levaquin (levofloxacin)'},
			{'index': 2, 'date': '11/2017'},
			{'index': 4, 'date': '04/2018'},
		]
		treatment1Edited = {
			'testMeta': {'type': 'antibiotics'},
			'questions': [
				{'type': 'single', 									# 0. Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',									# 1. Supportive Care Type
					'options': {
						'Antibiotics': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',									# 2. Antibiotics Type
					'options': {
						'Levaquin (levofloxacin)': {},
					},
				},
				{'type': 'date', 'text': '11/2017' }, # 3. Start date
				{'type': 'single', 										# 4. Still taking antibiotics?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 											# 5. Stop date
					'text': '04/2018',
					'actions': 'continue',
				},
			]
		}
		toView.edit_treatment(0, 'treatments', treatment1Edited, editValues)
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

		# Still taking antibiotics
		treatment2 = {
			'testMeta': {'type': 'antibiotics'},
			'questions': [
				{'type': 'single',										# 0. Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single', 										# 1. Supportive Care Type
					'options': {
						'Antibiotics': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',										# 2. Antibiotics Type
					'options': {
						'Biaxin (clarithromycin)': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # 3. Start date
				{'type': 'single',										# 4. Still taking antibiotics?
					'options': {
						'Yes': {},
					},
					'actions': 'continue',
				}
			]
		}
		self.assertTrue(toView.add_treatment(treatment2))
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

	def test_antifungal(self):
		''' test_add_treatment.py:TestExtra.test_antifungal '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		toView.delete_all_treatments()

		# Not currently taking antifungal
		treatment1 = {
			'testMeta': {'type': 'antifungal'},
			'questions': [
				{'type': 'single', 							# 0. Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',							# 1. Supportive Care Type
					'options': {
						'Anti-Fungal': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',							# 2. Anti-fungal Type
					'options': {
						'Amphotericin B': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # 3. Start date
				{'type': 'single',										# 4. Still taking antifungals?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 											# 5. Stop date
					'text': '02/2018',
					'actions': 'continue',
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment1))

		editValues = [
			{'num_questions': 5},
			{'index': 1, 'options': 'Itraconazole'},
			{'index': 2, 'date': '12/2017'},
			{'index': 4, 'date': '05/2018'},
		]
		treatment1Edited = {
			'testMeta': {'type': 'antifungal'},
			'questions': [
				{'type': 'single', 							# 0. Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',							# 1. Supportive Care Type
					'options': {
						'Anti-Fungal': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',							# 2. Anti-fungal Type
					'options': {
						'Itraconazole': {},
					},
				},
				{'type': 'date', 'text': '12/2017' }, # 3. Start date
				{'type': 'single',										# 4. Still taking antifungals?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 											# 5. Stop date
					'text': '05/2018',
					'actions': 'continue',
				},
			]
		}
		toView.edit_treatment(0, 'treatments', treatment1Edited, editValues)
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

		# Still taking antifungal
		treatment2 = {
			'testMeta': {'type': 'antifungal'},
			'questions': [
				{'type': 'single',								# 0. Treatment Type
					'options': {
						'Bone Strengtheners, Antibiotics and Anti Fungals (Optional)': {},
					},
				},
				{'type': 'single',								# 1. Supportive Care Type
					'options': {
						'Anti-Fungal': {},
					},
					'actions': 'continue',
				},
				{'type': 'single',								# 2. Anti-fungal Type
					'options': {
						'Amphotericin B': {},
					},
				},
				{'type': 'date', 'text': '10/2017' }, # 3. Start date
				{'type': 'single',										# 4. Still taking antifungals?
					'options': {
						'Yes': {},
					},
					'actions': 'continue',
				},
			]
		}
		self.assertTrue(toView.add_treatment(treatment2))
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

	def test_view_treatment_options(self):
		''' test_add_treatment.py:TestExtra.test_view_treatment_options '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		treatmentOptionsView = self.andrew.treatmentOptionsView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		toView.view_options()
		self.assertTrue(treatmentOptionsView.on())

@unittest.skip('wont pass')
class TestStemCell(unittest.TestCase):
	# 1. Treatment Type
	# 2. Stemcell Type
	# 3. Induction Therapy? (yes: +5)
	# 	Extra: Induction start date
	#   Extra: Current induction?
		# 	Extra: Induction stop date (if no)
	# 	Extra: Induction treatments
	# 	Extra: Changes to induction?
		# 	Extra: Added (if yes)
		# 	Extra: Removed (if yes)
	# 	Extra: Best Induction Response  (if yes)
	# 	Extra: Induction Side Effects (if yes)

	# 4. Transplant Start Date
	# 5. Dose of Melphalan
	# 6. Best Response to transplant
	# 7. Transplant SideEffects

	# 8. Maintenance therapy? (done if no)
	# 9. Maintenance: start date
	# 10. Currently on maintenance therapy?
	# 	Extra (No) Maintenance stop date
	# 11. Maintenance treatments
	# 12. Maintenance best response
	# 13. Maintenance sideEffects

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_basic(self):
		''' test_add_treatment.py::TestStemCell.test_basic '''
		# Only 8 questions. Not induction theraapy, not maintenance therapy
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())
		toView.delete_all_treatments()

		stemCellBasic = {
			'testMeta': {'type': 'stem cell'},
			'questions': [
				{'type': 'single', 							# 0. Treatment Type
					'options': {
						'Stem Cell Transplant': {},
					},
				},
				{'type': 'single',							# 1. Stem Cell type
					'options': {
						'Autologous (AUTO) Stem Cell Transplant': {},
					},
				},
				{'type': 'single',							# 2. Induction therapy?
					'options': {
						'No': {},
					},
				},
				{'name': 'transplant start date',								# 3. Transplant Start date
					'type': 'date',
					'text': '01/2018'
				},
				{'type': 'single',										# 4. Melphalan dose
					'options': {
						'No': {},
					},
				},
				{'type': 'single',										# 5. Response
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'popup', 										# 6: Side effects
					'options': {}
				},
				{'type': 'single',										# 7. Maintenance Therapy?
					'options': {
						'No': {},
					},
				},
			]
		}
		# self.assertTrue(toView.on({'tests': [stemCellBasic]}))
		self.assertTrue(toView.add_treatment(stemCellBasic))
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

		# Still taking induction (yes to question[4])
		# No drugs added/removed
		stemCellInduction = {
			'testMeta': {'type': 'stem cell'},
			'questions': [
				{'type': 'single', 							# 0. Treatment Type
					'options': {
						'Stem Cell Transplant': {},
					},
				},
				{'type': 'single',							# 1. Stem Cell type
					'options': {
						'Autologous (AUTO) Stem Cell Transplant': {},
					},
				},
				{'type': 'single',							# 2. Induction therapy?
					'options': {
						'Yes': {},
					},
				},
				{'type': 'date', 											# 3. Induction: Start date
					'text': '01/2018'
				},
				{'type': 'single',										# 4. Induction: Still taking?
					'options': {
						'Yes': {},
					},
				},
				{'type': 'popup', 										# 5: Induction: therapy treatments
					'options': {
						'Chemotherapies': {
							'Melphalan': {},
						}
					}
				},
				{'type': 'single',										# 6. Induction: Changes to therapy?
					'options': {
						'No': {},
					},
				},
				{'type': 'single',										# 7. Induction therapy Response
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'popup', 									# 8: Induction side effects
					'options': {
						'musculoskeletal system': {
		    			'Back pain': {},
		    		},
		    	}
				},


				{'name': 'transplant start date',								# 9. Transplant Start date
					'type': 'date',
					'text': '01/2018'
				},
				{'type': 'single',										# 10. Melphalan dose
					'options': {
						'No': {},
					},
				},
				{'type': 'single',										# 11. Response
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'popup', 										# 12: Side effects
					'options': {}
				},
				{'type': 'single',										# 13. Maintenance Therapy?
					'options': {
						'No': {},
					},
				},
			]
		}
		self.assertTrue(toView.add_treatment(stemCellInduction))
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

		# Still taking induction (no to question[4])
		# No drugs added/removed
		stemCellInduction = {
			'testMeta': {'type': 'stem cell'},
			'questions': [
				{'type': 'single', 							# 0. Treatment Type
					'options': {
						'Stem Cell Transplant': {},
					},
				},
				{'type': 'single',							# 1. Stem Cell type
					'options': {
						'Autologous (AUTO) Stem Cell Transplant': {},
					},
				},
				{'type': 'single',							# 2. Induction therapy?
					'options': {
						'Yes': {},
					},
				},
				{'type': 'date', 											# 3. Induction Start date
					'text': '01/2018'
				},
				{'type': 'single',										# 4. Still taking induction therapy?
					'options': {
						'No': {},
					},
				},
				{'type': 'date', 											# 5. Induction End date
					'text': '03/2018'
				},
				{'type': 'popup', 										# 6: Induction therapy treatments
					'options': {
						'Chemotherapies': {
							'Melphalan': {},
						}
					}
				},
				{'name': 'transplant start date',								# 7. Transplant Start date
					'type': 'date',
					'text': '01/2018'
				},
				{'type': 'single',										# 8. Melphalan dose
					'options': {
						'No': {},
					},
				},
				{'type': 'single',										# 9. Response
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'popup', 										# 10: Side effects
					'options': {}
				},
				{'type': 'single',										# 11. Maintenance Therapy?
					'options': {
						'No': {},
					},
				},
			]
		}
		self.assertTrue(toView.add_treatment(stemCellInduction))
		toView.edit_treatment(0, 'delete', {'meta': {'num_treatments': 0}})

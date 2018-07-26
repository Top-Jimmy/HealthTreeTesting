import unittest
import main
import initDriver
import profiles
import form_info
# import copy # copy.deepcopy(object)

# TestChemotherapy
# 	test_current_chemotherapy					Question[2] Are you currently taking chemotherapy?
# 	test_changed_chemotherapy: 				Question[5] Medications were added/removed during treatment?
# TestRadiation
# 	test_add_radiation
# TestExtra
# 	test_bone_strengthener: 					Question[4] still taking bone strengtheners?
# 	test_antibiotics: 								Question[4] Still taking antibiotics?
# 	test_antifungal: 									Question[4] still taking antifungal?
# TestStemCell
# 	test_basic_stem_cell
@unittest.skip('Add treatment crap')
class TestChemotherapy(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

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
				{'type': 'complex', # 4: Chemo treatment options
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
				{'type': 'single',	# 5: Changes to treatment?
					'options': {
						'No': {},
					},
				},
				{'type': 'single',	# 6: Best response?
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'complex', # 7: Side effects
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
				{'type': 'complex', # 5: Chemo treatment options
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
				{'type': 'complex', # 8: Side effects
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
				{'type': 'complex', # 4: Chemo treatment options
					'options': {
						'chemotherapies': {
		    			'Adriamycin': None,
		    		},
		    		'steroids': {
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
						'chemotherapies': {'melphalan': None,}
					}
				},
				{'type': 'table', # 7: Drugs REMOVED
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
				{'type': 'single',	# 8: Best response?
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'complex', # 9: Side effects
					'options': {
						'cardiovascular/circulatory system': {
		    			'blood clots': {'intensity': 9},
		    			'irregular/rapid heartbeat': {'intensity': 2},
		    		}
		    	}
				},
			]
		}
		# self.assertTrue(toView.on({'tests': [treatment1] }))
		self.assertTrue(toView.add_treatment(treatment1))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})
@unittest.skip('Add treatment crap')
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

		treatment1 = {
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
								'Cost of the treatment': {},
								'Too much travel': {},
								'Other': {'comment': 'Discontinued because Y'},
							},
						}
					},
					'actions': 'continue',
				},
				{'type': 'complex', 								# 5: Side effects
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
								'Other': {'comment': 'Discontinued comment: Treatment2'},
							},
						}
					},
					'actions': 'continue',
				},
				{'type': 'complex', 										# 5: Side effects
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

@unittest.skip('Add treatment crap')
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

		self.assertTrue(toView.add_treatment(treatment1, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

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
		self.assertTrue(toView.add_treatment(treatment2, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

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
		self.assertTrue(toView.add_treatment(treatment1, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

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
		self.assertTrue(toView.add_treatment(treatment2, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

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
		# Not currently taking antibiotics
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
		self.assertTrue(toView.add_treatment(treatment1, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

		# Still taking antibiotics
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
		self.assertTrue(toView.add_treatment(treatment2, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

	def test_view_treatment_options(self):
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
@unittest.skip('Add treatment crap')
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
		''' test_add_treatment.py:TestStemCell.test_basic '''
		# Only 8 questions. Not induction theraapy, not maintenance therapy
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		toView = self.andrew.treatmentsOutcomesView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Treatments & Outcomes')
		self.assertTrue(toView.on())

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
				{'type': 'complex', 										# 6: Side effects
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
		# self.assertTrue(toView.add_treatment(stemCellBasic, 'save'))
		# toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

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
				{'type': 'complex', 										# 5: Induction: therapy treatments
					'options': {
						'chemotherapies': {
							'melphalan': {},
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
				{'type': 'complex', 									# 8: Induction side effects
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
				{'type': 'complex', 										# 12: Side effects
					'options': {}
				},
				{'type': 'single',										# 13. Maintenance Therapy?
					'options': {
						'No': {},
					},
				},
			]
		}
		self.assertTrue(toView.add_treatment(stemCellInduction, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

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
				{'type': 'date', 											# 3. Induction End date
					'text': '03/2018'
				},
				{'type': 'complex', 										# 5: Induction therapy treatments
					'options': {
						'chemotherapies': {
							'melphalan': {},
						}
					}
				},
				{'name': 'transplant start date',								# 6. Transplant Start date
					'type': 'date',
					'text': '01/2018'
				},
				{'type': 'single',										# 7. Melphalan dose
					'options': {
						'No': {},
					},
				},
				{'type': 'single',										# 8. Response
					'options': {
						'The treatment did not reduce my myeloma': {},
					},
				},
				{'type': 'complex', 										# 9: Side effects
					'options': {}
				},
				{'type': 'single',										# 10. Maintenance Therapy?
					'options': {
						'No': {},
					},
				},
			]
		}
		self.assertTrue(toView.add_treatment(stemCellInduction, 'save'))
		toView.edit(0, 'delete', {'meta': {'num_treatments': 0}})

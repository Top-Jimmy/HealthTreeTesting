import unittest
import main
import initDriver
import profiles

class TestMyelomaGenetics(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		'''MyelomaGenetics : MyelomaGenetics . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaGeneticsView = self.andrew.myelomaGeneticsView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Genetics')
		self.assertTrue(myelomaGeneticsView.on())

	def test_add_fish(self):

		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaGeneticsView = self.andrew.myelomaGeneticsView
		fishInfo = {
			'test_fish_date': '06/2018',
			'gene_additions': [
				{'3copies': False}, {'4copies': False}
			],
			'three_1q21': True,
			'four_1q21': True,
			'deletion_1p': False,
			'deletion_17p': True,
			'deletion_13q': False,
			'deletion_16q': True,
			'trans_FGFR3': True,
			'trans_CCND3': True,
			'trans_CCND1': False,
			'trans_cMAF': True,
			'trans_MAFB': False,
			'trans_ETV6': True,
			'tri_3': True,
			'tri_5': False,
			'tri_7': True,
			'tri_9': True,
			'tri_11': False,
			'tri_15': True,
			'tri_17': True,
			'tri_19': True,
			'tetra_3': True,
			'tetra_5': False,
			'tetra_7': False,
			'tetra_9': False,
			'tetra_11': True,
			'tetra_15': True,
			'tetra_17': False,
			'tetra_19': True,
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Genetics')
		self.assertTrue(myelomaGeneticsView.on())

		# add fish test should automatically reload page
		myelomaGeneticsView.add_fish_test(fishInfo)

		self.assertTrue(myelomaGeneticsView.on())

		# riskInfo = {
		# 	'high_b2m': 'Yes',
		# 	'high_ldh': 'I dont know',
		# 	'low_albumin': 'I dont know',
		# }

		# myelomaGeneticsView.edit_high_risk(riskInfo, 'save')

		# self.assertTrue(myelomaGeneticsView.on())

	def test_add_gep(self):

		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaGeneticsView = self.andrew.myelomaGeneticsView
		gepInfo = {
			'test_gep_date': '04/2013',
			'gep_comment': 'Doubts about validity',
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Genetics')
		self.assertTrue(myelomaGeneticsView.on())

		myelomaGeneticsView.add_gep_test(gepInfo)

		self.assertTrue(myelomaGeneticsView.on())

	def test_add_ngs(self):

		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaGeneticsView = self.andrew.myelomaGeneticsView
		ngsInfo = {
			'test_ngs_date': '11/2010',
			'ngs_comment': 'jkl',
			'mutate_nras': False,
			'mutate_kras': True,
			'mutate_braf': True,
			'mutate_tp53': False,
			'mutate_fam46c': True,
			'mutate_dis3': False,
			'mutate_traf3': True,
			'mutate_fgfr3': True,
			'mutate_atm': False,
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Genetics')
		self.assertTrue(myelomaGeneticsView.on())

		myelomaGeneticsView.add_ngs_test(ngsInfo)

		self.assertTrue(myelomaGeneticsView.on())

		riskInfo = {
			'high_b2m': 'Yes',
			'high_ldh': 'I dont know',
			'low_albumin': 'I dont know',
		}

		myelomaGeneticsView.edit_high_risk(riskInfo)

		self.assertTrue(myelomaGeneticsView.on())






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

		myelomaGeneticsView.add_fish_test(fishInfo, 'save')






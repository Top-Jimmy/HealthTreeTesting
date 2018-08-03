import unittest
import main
import initDriver
import profiles

class TestMyelomaLabs(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		'''MyelomaLabs : MyelomaLabs . test_navigate'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaLabsView = self.andrew.myelomaLabsView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Labs')
		self.assertTrue(myelomaLabsView.on())

	def test_add_lab(self):
		'''MyelomaLabs : MyelomaLabs . test_add_lab'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaLabsView = self.andrew.myelomaLabsView

		labInfo = {
			'dobd': '12/12/2013',
			'monoclonal': '14',
			'kappa': '234',
			'lambda': '457',
			'ratio': '2',
			'bone_marrow': '15',
			'blood': '8435',
			'calcium': '78345',
			'platelets': '3',
			'blood_cell': '90',
			'hemoglobin': '798',
			'lactate': '532',
			'immuno_g': '275',
			'immuno_a': '97969765',
			'immuno_m': '7459',
			'albumin': '539',
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Labs')
		self.assertTrue(myelomaLabsView.on())

		myelomaLabsView.add_new_lab(labInfo, 'save')

		self.assertTrue(myelomaLabsView.on())

		myelomaLabsView.edit_delete_lab(-1, None, 'delete', 'confirm')

	def test_edit_lab(self):
		'''MyelomaLabs : MyelomaLabs . test_edit_lab'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaLabsView = self.andrew.myelomaLabsView

		labInfo = {
			'dobd': '12/12/2013',
			'monoclonal': '14',
			'kappa': '234',
			'lambda': '457',
			'ratio': '2',
			'blood': '8435',
			'calcium': '78345',
			'platelets': '3',
			'blood_cell': '90',
			'hemoglobin': '798',
			'lactate': '532',
			'immuno_g': '275',
			'immuno_a': '97969765',
			'immuno_m': '7459',
			'albumin': '539',
		}

		revisedLabInfo = {
			'dobd': '12/14/2017',
			'monoclonal': '19',
			'kappa': '234',
			'lambda': '457',
			'ratio': '2',
			'bone_marrow': '15',
			'blood': '8435',
			'calcium': '0',
			'platelets': '3',
			'blood_cell': '90',
			'hemoglobin': '23',
			'lactate': '532',
			'immuno_g': '275',
			'immuno_a': '43',
			'immuno_m': '7459',
			'albumin': '539',
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Labs')
		self.assertTrue(myelomaLabsView.on())

		myelomaLabsView.add_new_lab(labInfo, 'save')

		self.assertTrue(myelomaLabsView.on())

		myelomaLabsView.edit_delete_lab(-1, revisedLabInfo, 'edit')



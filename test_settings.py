import unittest
import main
import initDriver
import profiles
import time
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestSettings(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.elliot = profiles.Profile(self.driver, 'elliot')

	def tearDown(self):
		self.driver.quit()

	def test_navigate(self):
		'''settings : settings . test_navigate'''
		homeView = self.elliot.homeView
		aboutMeView = self.elliot.aboutMeView
		settingsView = self.elliot.settingsView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.elliot.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Settings')
		
		self.assertTrue(settingsView.on())

	def test_change_username(self):
		'''settings : settings . test_change_username'''
		homeView = self.elliot.homeView
		aboutMeView = self.elliot.aboutMeView
		settingsView = self.elliot.settingsView

		usernameInfo = {
			'new_username': 'elliot1'
		}

		passwordInfo = {
			'username': 'Elliot1',
			'password': 'cardinals',
			'old_password': 'celtics',
			'new_password': 'cardinals'
		}

		otherusernameInfo = {
			'new_username': 'Elliot'
		}

		otherpasswordInfo = {
			'username': 'Elliot',
			'password': 'celtics',
			'old_password': 'cardinals',
			'new_password': 'celtics'
		}

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.elliot.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Settings')

		self.assertTrue(settingsView.on())
		settingsView.change_username(usernameInfo, 'continue')
		self.assertTrue(settingsView.on())
		settingsView.change_password(passwordInfo, 'continue')

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(passwordInfo))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Settings')

		self.assertTrue(settingsView.on())
		settingsView.change_username(otherusernameInfo, 'continue')
		self.assertTrue(settingsView.on())
		settingsView.change_password(otherpasswordInfo, 'continue')

	def test_change_email(self):
		'''settings : settings . test_change_email'''
		homeView = self.elliot.homeView
		aboutMeView = self.elliot.aboutMeView
		settingsView = self.elliot.settingsView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.elliot.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Settings')
		
		self.assertTrue(settingsView.on())

		formData = {
			'password': 'celtics',
			'new_email': 'leonardbuttkiss123@hotmail.com'
		}

		settingsView.change_email(formData, 'continue', 'cancel')
		self.assertTrue(settingsView.on())


import unittest
import main
import initDriver
import profiles

# Create Account
# Forgot Password
# Login

class TestCreateAccount(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_invalid_credentials(self):
		'''Authentication : CreateAcct . test_invalid_credentials'''
		pass

	def test_errors(self):
		# relevant ??
		pass

	def test_navigation(self):
		'''Authentication : CreateAcct . test_navigation'''
		homeView = self.andrew.homeView
		createAcctView = self.andrew.createAcctView

		self.assertTrue(createAcctView.go())

	def test_success(self):
		'''Authentication : CreateAcct . test_success'''
		pass

	def test_create_account(self):
		'''Authentication : CreateAcct . test_create_account'''
		homeView = self.andrew.homeView
		createAcctView = self.andrew.createAcctView

		self.assertTrue(createAcctView.go())


class TestForgotPassword(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_invalid_credentials(self):
		'''Authentication : ForgotPassword . test_invalid_credentials'''
		forgotPwView = self.andrew.forgotPwView
		bogus_email = 'invalid'
		self.assertTrue(forgotPwView.go())
		self.assertTrue(forgotPwView.reset_password(bogus_email, expectedWarning='invalid credentials'))

	def test_navigation(self):
		'''Authentication : ForgotPassword . test_navigation'''
		homeView = self.andrew.homeView
		forgotPwView = self.andrew.forgotPwView

		self.assertTrue(homeView.go())
		homeView.click_link('forgot password')
		self.assertTrue(forgotPwView.on())
		forgotPwView.click_link('sign in')
		self.assertTrue(homeView.on())

	def test_success(self):
		'''Authentication : ForgotPassword . test_success'''
		# Todo
		pass

class TestLogin(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_errors(self):
		'''Authentication : Login . test_error_confirmation'''
		homeView = self.andrew.homeView
		bogusCredentials = {
			'username': 'Drew',
			'password': 'invalid',
		}

		self.assertTrue(homeView.go())
		# Are login credentials associated with validated email? (only fails on production)
		if main.env == 'prod':
			self.assertTrue(homeView.login(self.andrew.credentials, expectedError='confirmation'))
		# Using invalid credentials?
		self.assertTrue(homeView.login(bogusCredentials, expectedError='invalid credentials'))

	def test_success(self):
		'''Authentication : Login . test_success'''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))

		self.assertTrue(aboutMeView.on())
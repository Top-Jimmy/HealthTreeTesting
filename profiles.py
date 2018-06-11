from Views import *
import credentials

class Profile:
  def __init__(self, driver, name=None):
  	self.driver = driver
  	self.credentials = credentials.get_credentials(name)

  	# Public Views
  	self.homeView = homeView.HomeView(driver)
  	self.forgotPwView = forgotPwView.ForgotPwView(driver)
  	self.createAcctView = createAcctView.CreateAcctView(driver)

  	# Authenticated
  	self.aboutMeView = aboutMeView.AboutMeView(driver)
  	self.myelDiagView = myelDiagView.MyelDiagView(driver)
  	self.currentHealthView = currentHealthView.CurrentHealthView(driver)
  	self.fitLvlView = fitLvlView.FitLvlView(driver)
  	self.fullHealthView = fullHealthView.FullHealthView(driver)

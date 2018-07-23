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
		self.myelomaDiagnosisView = myelDiagView.MyelDiagView(driver)
		self.currentHealthView = currentHealthView.CurrentHealthView(driver)
		self.fitLvlView = fitLvlView.FitLvlView(driver)
		self.fullHealthView = fullHealthView.FullHealthView(driver)
		self.myelomaGeneticsView = myelomaGeneticsView.MyelomaGeneticsView(driver)
		self.treatmentsOutcomesView = treatmentsOutcomesView.TreatmentsOutcomesView(driver)

		# Myeloma Labs
		self.myelomaLabsView = myelomaLabsView.MyelomaLabsView(driver)
		self.myLabsFacilitiesView = myLabsFacilitiesView.MyLabsFacilitiesView(driver)
		self.myLabsAddFacilityView = myLabsAddFacilityView.MyLabsAddFacilityView(driver)
		self.consentFormView = consentFormView.ConsentFormView(driver)

		self.settingsView = settingsView.SettingsView(driver)
		self.surveysView = surveysView.SurveysView(driver)


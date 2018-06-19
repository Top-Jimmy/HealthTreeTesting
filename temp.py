import profiles
import time
import main
import initDriver

def date_picker_unittest():
	self.driver = initDriver.start(main.browser)
	self.andrew = profiles.Profile(self.driver, 'andrew')

	homeView = self.andrew.homeView
	aboutMeView = self.andrew.aboutMeView

	# Go to myeloma Diagnosis page
	self.assertTrue(homeView.go())
	self.assertTrue(homeView.login(self.andrew.credentials))
	self.assertTrue(aboutMeView.on())
	aboutMeView.menu.go_to('Myeloma Diagnosis')
	self.assertTrue(myelDiagView.on('fresh'))

	#

if __name__ == '__main__':
  date_picker_unittest()


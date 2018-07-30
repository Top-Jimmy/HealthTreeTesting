import unittest
import main
import initDriver
import profiles

class TestGetMyLabs(unittest.TestCase):

  def setUp(self):
    self.driver = initDriver.start(main.browser)
    self.andrew = profiles.Profile(self.driver, 'andrew')

  def tearDown(self):
    self.driver.quit()

  def test_navigate(self):
    ''' test_get_my_labs.py:TestGetMyLabs.test_navigate '''
    # months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    # for month in months:
    #   raw_input(month + ': ' + str(int(month)))
    # raw_input('?')

    homeView = self.andrew.homeView
    aboutMeView = self.andrew.aboutMeView
    myelomaLabsView = self.andrew.myelomaLabsView
    myLabs_facilities = self.andrew.myLabsFacilitiesView
    myLabs_add_facility = self.andrew.myLabsAddFacilityView
    consent_form = self.andrew.consentFormView
    facility_name = 'Test Facility'
    form_preferences = ['access_all_records', 'lab_reports', 'history', 'admission', 'medication',
      'xray', 'paperwork', 'consult', 'mental', 'alcohol', 'hiv', 'other']
    other_comment = 'Other records'
    patient_info = {
      'first name': 'Test',
      'last name': 'User',
      'rep first name': 'Representative',
      'rep last name': 'LastName',
      'date': '01/23/2015',
    }
    portal_info = {
      'username': 'BogusUser',
      'password': 'asdfasdf',
      'url': 'www.portalURL.com',
    }

    self.assertTrue(homeView.go())
    self.assertTrue(homeView.login(self.andrew.credentials))
    self.assertTrue(aboutMeView.on())

    aboutMeView.menu.go_to('Myeloma Labs')
    self.assertTrue(myelomaLabsView.on())
    myelomaLabsView.get_my_labs()
    self.assertTrue(myLabs_facilities.on())
    num_facilities = myLabs_facilities.num_facilities()
    myLabs_facilities.add_facility_button.click()

    self.assertTrue(myLabs_add_facility.on())
    myLabs_add_facility.set_facility(facility_name)
    self.assertTrue(consent_form.on())

    # Consent Form
    self.assertEqual(facility_name, consent_form.facility_name)
    consent_form.set_preferences(form_preferences, other_comment)
    # Should undo selection of 'all'
    self.assertEqual(form_preferences[1:], consent_form.get_preferences())
    self.assertEqual(other_comment, consent_form.other_input.get_attribute('value'))
    consent_form.set_patient_info(patient_info, 'picker')
    self.assertEqual(patient_info, consent_form.get_patient_info())
    consent_form.set_portal_info(portal_info)
    self.assertEqual(portal_info, consent_form.get_portal_info())

    consent_form.action('submit')

    # Verify number of facilities, then delete them all
    self.assertTrue(myLabs_facilities.on())
    self.assertEqual(num_facilities+1, myLabs_facilities.num_facilities())
    myLabs_facilities.delete_all()





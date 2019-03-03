import unittest
import main
import initDriver
import profiles
import time
import datetime

class TestGetMyLabs(unittest.TestCase):

	def setUp(self):
		self.driver = initDriver.start(main.browser)
		self.andrew = profiles.Profile(self.driver, 'andrew')

	def tearDown(self):
		self.driver.quit()

	def test_datepicker(self):
		''' test_get_my_labs.py:TestGetMyLabs.test_datepicker '''
		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaLabsView = self.andrew.myelomaLabsView
		myLabs_facilities = self.andrew.myLabsFacilitiesView
		myLabs_add_facility = self.andrew.myLabsAddFacilityView
		consent_form = self.andrew.consentFormView
		facility_name = 'Test Datepicker Facility'
		typed_date = '10/09/2017'
		now = datetime.datetime.now()

		self.assertTrue(homeView.go())
		self.assertTrue(homeView.login(self.andrew.credentials))
		self.assertTrue(aboutMeView.on())

		aboutMeView.menu.go_to('Myeloma Labs')
		self.assertTrue(myelomaLabsView.on())
		myelomaLabsView.get_my_labs()
		self.assertTrue(myLabs_facilities.on())
		myLabs_facilities.delete_all()
		myLabs_facilities.add_facility_button.click()

		self.assertTrue(myLabs_add_facility.on())
		myLabs_add_facility.set_facility(facility_name)
		# time.sleep(2)
		self.assertTrue(consent_form.on())

		# Verify datepicker defaults to current month/year (no day selected)
		self.assertTrue(consent_form.compare_date(now.strftime("%m//%Y"), 'picker'))

		# Type a date into input
		consent_form.set_date(typed_date, 'picker')

		# Verify datepicker shows date
		self.assertTrue(consent_form.compare_date(typed_date, 'picker'))

		# Clear out input
		consent_form.set_date('')

		# Verify datepicker still has month/year of old date
		self.assertTrue(consent_form.compare_date("10//2017", 'picker'))

		# Enter current date via picker, Verify
		consent_form.set_date(now.strftime("%m/%d/%Y"), 'picker')
		self.assertTrue(consent_form.compare_date(now.strftime("%m/%d/%Y"), 'picker'))

	def test_edit(self):
		''' test_get_my_labs.py:TestGetMyLabs.test_edit '''
		# 1. Add and save facility
		# 2. Edit and verify it has original data
		# 3. Change and save. Verify it keeps changes

		homeView = self.andrew.homeView
		aboutMeView = self.andrew.aboutMeView
		myelomaLabsView = self.andrew.myelomaLabsView
		myLabs_facilities = self.andrew.myLabsFacilitiesView
		myLabs_add_facility = self.andrew.myLabsAddFacilityView
		consent_form = self.andrew.consentFormView
		facility_name = 'Edit Facility'
		form_preferences = ['lab_reports', 'history', 'admission', 'medication',
			'xray', 'paperwork', 'consult', 'mental', 'alcohol', 'hiv', 'other']
		other_comment = 'Other records'
		patient_info = {
			'first name': 'Test',
			'last name': 'User',
			'rep first name': 'Representative',
			'rep last name': 'LastName',
			'date': 'current',
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
		myLabs_facilities.delete_all()
		myLabs_facilities.add_facility_button.click()

		self.assertTrue(myLabs_add_facility.on())
		myLabs_add_facility.set_facility(facility_name)
		# time.sleep(2)
		raw_input('?')
		self.assertTrue(consent_form.on())

		# 1. Add and save facility
		self.assertEqual(facility_name, consent_form.facility_name)
		# Set 'All records' option
		consent_form.set_preferences(['access_all_records'])
		self.assertEqual(['access_all_records'], consent_form.get_preferences())
		# Set all individual preferences
		consent_form.set_preferences(form_preferences, other_comment)
		self.assertEqual(form_preferences, consent_form.get_preferences())

		self.assertEqual(other_comment, consent_form.other_input.get_attribute('value'))
		consent_form.set_patient_info(patient_info, 'picker')
		self.assertEqual(patient_info, consent_form.get_patient_info())
		consent_form.set_portal_info(portal_info)
		self.assertEqual(portal_info, consent_form.get_portal_info())
		consent_form.action('submit')
		raw_input('on my labs?')
		match = False
		count = 0
		while not match and count < 5:
			self.assertTrue(myLabs_facilities.on())
			if myLabs_facilities.num_facilities() == 1:
					match = True
			else:
					print(str(count) + ' Expected 1 facility. Loaded ' + str(myLabs_facilities.num_facilities()))
			count += 1
			time.sleep(.4)


		# 2. Edit and verify it has original data
		self.assertTrue(myLabs_facilities.manage_facility(0, 'edit'))
		time.sleep(2) # Wait for edit values to show up
		self.assertTrue(consent_form.on(None, True))

		# Check preferences, comment, patient_info, portal_info
		self.assertEqual(form_preferences, consent_form.get_preferences())
		# Should clear out 'other' comment (currently does not #939)
		# self.assertEqual('', consent_form.other_input.get_attribute('value'))
		self.assertEqual(patient_info, consent_form.get_patient_info())
		# Password will be all * characters
		hidden_password = '*' * len(portal_info['password'])
		portal_info['password'] = hidden_password
		self.assertEqual(portal_info, consent_form.get_portal_info())

		# Click portal_info edit button and verify info (password should be empty)
		portal_info['password'] = ''
		consent_form.edit_login_info_button.click()
		self.assertTrue(consent_form.on(None, True))
		self.assertEqual(portal_info, consent_form.get_portal_info())


		# 3. Change and save. Verify it keeps changes
		new_preferences = form_preferences[:5]
		new_patient_info = {
			'first name': 'Tester',
			'last name': 'EditedUser',
			'rep first name': 'Edited',
			'rep last name': 'Representative',
			'date': '02/23/2018',
		}
		# Should clear out patient NAME and DATE if preferences are changed
		edited_patient_info = { 
			'first name': '',
			'last name': '',
			'rep first name': 'Representative',
			'rep last name': 'LastName',
			'date': 'current',
		}
		new_portal_info = {
			'username': 'EditedUser',
			'password': 'asdfasdf2',
			'url': 'www.editedPortalURL.com',
		}

		consent_form.set_preferences(new_preferences)
		self.assertEqual(new_preferences, consent_form.get_preferences())
		# Should clear out 'other' comment (currently does not #939)
		# self.assertEqual('', consent_form.other_input.get_attribute('value'))

		# Should clear out patient name if preferences are changed
		self.assertEqual(edited_patient_info, consent_form.get_patient_info())

		consent_form.set_patient_info(new_patient_info, 'picker')
		self.assertEqual(new_patient_info, consent_form.get_patient_info(current_date=False))
		consent_form.set_portal_info(new_portal_info)
		self.assertEqual(new_portal_info, consent_form.get_portal_info())

		consent_form.action('submit')

		# Edit consent form and verify it has edited data
		self.assertTrue(myLabs_facilities.on())
		self.assertTrue(myLabs_facilities.manage_facility(0, 'edit'))
		self.assertTrue(consent_form.on(None, True))

		# Check preferences, comment, patient_info, portal_info
		self.assertEqual(new_preferences, consent_form.get_preferences())
		self.assertEqual(new_patient_info, consent_form.get_patient_info(current_date=False))
		# Password will be all * characters
		hidden_password = '*' * len(new_portal_info['password'])
		new_portal_info['password'] = hidden_password
		self.assertEqual(portal_info, consent_form.get_portal_info())

		# Click portal_info edit button and verify info (password should be empty)
		new_portal_info['password'] = ''
		consent_form.edit_login_info_button.click()
		self.assertTrue(consent_form.on(None, True))
		self.assertEqual(new_portal_info, consent_form.get_portal_info())

		# Click 'I don't agree button' and land on myLabs_facilities
		consent_form.action('do not agree')
		self.assertTrue(myLabs_facilities.on())
		myLabs_facilities.delete_all()

	def test_navigate(self):
		''' test_get_my_labs.py:TestGetMyLabs.test_navigate '''

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
			'date': 'current',
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
		# time.sleep(2)
		self.assertTrue(consent_form.on())

		# Consent Form: Check every box (except 'all') and add 'other' comment
		self.assertEqual(facility_name, consent_form.facility_name)
		consent_form.set_preferences(form_preferences[1:], other_comment)
		self.assertEqual(form_preferences[1:], consent_form.get_preferences())
		self.assertEqual(other_comment, consent_form.other_input.get_attribute('value'))
		# Select 'all': should undo all other selections and clear out 'other' comment
		consent_form.set_preferences(form_preferences[:1])
		self.assertEqual(form_preferences[:1], consent_form.get_preferences())
		self.assertEqual('', consent_form.other_input.get_attribute('value'))
		
		# Set patient info: Type date
		# consent_form.set_patient_info(patient_info, 'typed')
		# self.assertEqual(patient_info, consent_form.get_patient_info())
		# Set current date via picker. Check that date == current date
		consent_form.set_patient_info(patient_info, 'picker')
		self.assertEqual(patient_info, consent_form.get_patient_info())

		# Portal Info
		consent_form.set_portal_info(portal_info)
		self.assertEqual(portal_info, consent_form.get_portal_info())

		consent_form.action('submit')

		# Verify number of facilities, then delete them all
		# Can take a few seconds for new facility to show up.
		match = False
		count = 0
		while not match and count < 5:
				self.assertTrue(myLabs_facilities.on())
				if num_facilities + 1 == myLabs_facilities.num_facilities():
						match = True
				else:
						print(str(count) + ' Expected ' + str(num_facilities + 1) + ' facilities. Loaded ' + str(myLabs_facilities.num_facilities()))
				count += 1
				time.sleep(.4)

		self.assertEqual(num_facilities+1, myLabs_facilities.num_facilities())
		myLabs_facilities.delete_all()






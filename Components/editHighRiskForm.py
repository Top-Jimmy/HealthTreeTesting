from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException, ElementNotVisibleException)


class EditHighRiskForm():

	def __init__(self, driver):
		self.driver = driver

	def load(self):
		self.form = self.driver.find_elements_by_tag_name('form')[1]
		buttons = self.form.find_elements_by_tag_name('button')

		# self.close_button = buttons[5]
		self.high_b2m_yes_radio = self.form.find_element_by_id('high_b2m_1_div')
		self.high_b2m_no_radio = self.form.find_element_by_id('high_b2m_2_div')
		self.high_b2m_idk_radio = self.form.find_element_by_id('high_b2m_3_div')

		self.high_ldh_yes_radio = self.form.find_element_by_id('high_ldh_1_div')
		self.high_ldh_no_radio = self.form.find_element_by_id('high_ldh_2_div')
		self.high_ldh_idk_radio = self.form.find_element_by_id('high_ldh_3_div')

		self.low_albumin_yes_radio = self.form.find_element_by_id('low_albumin_1_div')
		self.low_albumin_no_radio = self.form.find_element_by_id('low_albumin_2_div')
		self.low_albumin_idk_radio = self.form.find_element_by_id('low_albumin_3_div')

		self.save_button = buttons[1]
		self.cancel_button = buttons[0]

		return True
		# return self.validate(expectedValues)
	def validate(self, expectedValues):
		failures = []
		if expectedValues:
			if expectedValues['high_b2m'] == 'I dont know' and not self.high_ldh_idk_radio.get_attribute('checked'):
				failure.append('EditHighRiskForm: Expecting "I dont know" to having high B2M')
			if expectedValues['high_b2m'] == 'Yes' and not self.high_ldh_yes_radio.get_attribute('checked'):
				failure.append('EditHighRiskForm: Expecting "Yes" to having high B2M')
			if expectedValues['high_b2m'] == 'No' and not self.high_ldh_no_radio.get_attribute('checked'):
				failure.append('EditHighRiskForm: Expecting "No" to having high B2M')

			if expectedValues['high_ldh'] == 'I dont know' and not self.high_ldh_idk_radio.get_attribute('checked'):
				failure.append('EditHighRiskForm: Expecting "I dont know" to having high LDH')
			if expectedValues['high_ldh'] == 'Yes' and not self.high_ldh_yes_radio.get_attribute('checked'):
				failure.append('EditHighRiskForm: Expecting "Yes" to having high LDH')
			if expectedValues['high_ldh'] == 'No' and not self.high_ldh_no_radio.get_attribute('checked'):
				failure.append('EditHighRiskForm: Expecting "No" to having high LDH')

			if expectedValues['low_albumin'] == 'I dont know' and not self.low_albumin_idk_radio.get_attribute('checked'):
				failure.append('EditHighRiskForm: Expecting "I dont know" to having low albumin')
			if expectedValues['low_albumin'] == 'Yes' and not self.low_albumin_yes_radio.get_attribute('checked'):
				failure.append('EditHighRiskForm: Expecting "Yes" to having low albumin')
			if expectedValues['low_albumin'] == 'No' and not self.low_albumin_no_radio.get_attribute('checked'):
				failure.append('EditHighRiskForm: Expecting "No" to having low albumin')

	def submit(self, riskInfo, action='save'):
		if riskInfo:
			if riskInfo['high_b2m'] == 'yes':
				self.high_b2m_yes_radio.click()
			elif riskInfo['high_b2m'] == 'no':
				self.high_b2m_no_radio.click()
			else:
				self.high_b2m_idk_radio.click()

			if riskInfo['high_ldh'] == 'yes':
				self.high_ldh_yes_radio.click()
			elif riskInfo['high_ldh'] == 'no':
				self.high_ldh_no_radio.click()
			else:
				self.high_ldh_idk_radio.click()

			if riskInfo['low_albumin'] == 'yes':
				self.low_albumin_yes_radio.click()
			elif riskInfo['low_albumin'] == 'no':
				self.low_albumin_no_radio.click()
			else:
				self.low_albumin_idk_radio.click()

			if action == 'save':
				self.save_button.click()
			if action == 'cancel':
				self.cancel_button.click()
			if action == 'close':
				self.close_button.click()
			return True
		return False



# ############ Saved Form ############
#  def edit_fish_test(self)

 	

				



	# def confirm(self, action='submit'):
	# 	if action == 'submit':
	# 		self.confirm_button.click()
	# 	else:
	# 		self.cancel_button.click()
	# 	return True


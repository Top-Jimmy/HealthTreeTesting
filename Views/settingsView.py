from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from viewExceptions import MsgError, WarningError
from Components import aboutMeForm
from Components import menu
from Components import header
from Components import changeUsernameForm
from Components import changePasswordForm
from Views import view
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class SettingsView(view.View):
	post_url = 'settings'

	def load(self, formInfo=None):
		try:
			WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
			self.menu = menu.Menu(self.driver)
			self.header = header.AuthHeader(self.driver)

			form = self.driver.find_elements_by_tag_name('form')[-1]
			buttons = form.find_elements_by_tag_name('button')

			self.edit_username_button = buttons[0]
			self.edit_password_button = buttons[1]
			# self.validate()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	# def validate(self):
	# 	failures = []
	def change_username(self, usernameInfo, action='continue'):
		self.edit_username_button.click()
		self.changeUsernameForm = changeUsernameForm.ChangeUsernameForm(self.driver)
		WDW(self.driver, 20).until(lambda x: self.changeUsernameForm.load())
		self.changeUsernameForm.submit(usernameInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def change_password(self, passwordInfo, action='continue'):
		self.edit_password_button.click()
		self.changePasswordForm = changePasswordForm.ChangePasswordForm(self.driver)
		WDW(self.driver, 20).until(lambda x: self.changePasswordForm.load())
		self.changePasswordForm.submit(passwordInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.header = header.AuthHeader(self.driver)
		self.header.logout_button.click()

	def change_back_username(self, otherusernameInfo, action='continue'):
		self.edit_username_button.click()
		self.changeUsernameForm = changeUsernameForm.ChangeUsernameForm(self.driver)
		WDW(self.driver, 20).until(lambda x: self.changeUsernameForm.load())
		self.changeUsernameForm.submit(otherusernameInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))

	def change_back_password(self, otherpasswordInfo, action='continue'):
		self.edit_password_button.click()
		self.changePasswordForm = changePasswordForm.ChangePasswordForm(self.driver)
		WDW(self.driver, 20).until(lambda x: self.changePasswordForm.load())
		self.changePasswordForm.submit(otherpasswordInfo, action)
		WDW(self.driver, 3).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
		WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'overlay')))
		self.header = header.AuthHeader(self.driver)
		self.header.logout_button.click()
	
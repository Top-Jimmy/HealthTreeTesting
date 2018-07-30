from selenium.common.exceptions import WebDriverException
import time

class Menu():

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.cont = self.driver.find_element_by_id('sidebar-wrapper')
		self.form = self.cont.find_element_by_tag_name('form')
		self.list_items = self.form.find_elements_by_tag_name('li')
		self.menu_options = {}

		# Loading full menu or basic menu for new user?
		self.menu_type = self.calculate_menu_type()

		if len(self.list_items) < 14 or len(self.list_items) > 15:
			print('Unexpected # of menu items, menu has ' + str(len(self.list_items)))
			return False

		for i, option in enumerate(self.list_items):
			if 'Surveys' in option.text:
				self.menu_options['Surveys'] = self.list_items[i]
			else:
				self.menu_options[option.text] = self.list_items[i]
		return True

	def calculate_menu_type(self):
		menuType = 'new'
		if len(self.list_items) > 10:
			menuType = 'normal'
		return menuType

	def go_to(self, destination):
		"""Go to given page in menu. Destination should match text in menu."""
		option = self.menu_options[destination]
		if option:
			self.driver.execute_script('arguments[0].scrollIntoView();', option)
			try:
				option.click()
			except WebDriverException:
				print('failed to click menu item.')
				time.sleep(.4)
				self.go_to(destination)
		else:
			print('Menu: Unexpected destination: ' + destination)
			return False

	def selected_option(self):
		self.menu_items = []
		lists = self.cont.find_elements_by_tag_name('li')
		for i, li in enumerate(lists):
			classes = li.get_attribute('class')
			if 'active' in classes:
				self.menu_items.append(lists[i].text)

		print(self.menu_items)



def move_to_el(self, el, click=True):
		self.driver.execute_script('arguments[0].scrollIntoView();', el)
		time.sleep(.6)
		if click:
			try:
				el.click()
				return True
			except WebDriverException:
				pass
		return False
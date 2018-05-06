# -*- encoding: utf-8 -*-

##############################################################################
#
##############################################################################

	def register_vk(self):
		self.browser.visit('http://m.vk.com/join')
		self.browser.find_by_name('first_name').last.fill(self.first_name)
		self.browser.find_by_name('last_name').last.fill(self.last_name)	
		self.browser.find_by_xpath('//input[@type="submit"]').click()
		
		time.sleep(5)
		
		if 'act=start' in self.browser.url:
			val = raw_input("Inter capture: ")
			
			self.browser.find_by_name('captcha_key').last.fill(val)
			self.browser.find_by_xpath('//input[@type="submit"]').click()
			
		self.browser.find_by_name('phone').last.fill('+7'+self.vk_phone)
		self.browser.find_by_xpath('//input[@type="submit"]').click()
		
		val = raw_input("Inter VK SMS code: ")
		self.browser.find_by_name('code').last.fill(val)
		self.browser.find_by_xpath('//input[@type="submit"]').click()
		
		self.browser.find_by_name('pass').last.fill(self.password)
		self.browser.find_by_xpath('//input[@type="submit"]').click()
		
		self.browser.find_by_xpath('//div[@class="profile_photo_upload"]').first.click()
		
		self.browser.attach_file('photo', self.photo_path)
		self.browser.find_by_xpath('//input[@type="submit"]').click()
		
		self.profile_vk()
		
	def profile_vk(self):
		self.browser.visit('http://m.vk.com')

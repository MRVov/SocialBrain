# -*- encoding: utf-8 -*-

##############################################################################
#
#
##############################################################################

	def register_facebook(self):
		self.browser.visit('https://m.facebook.com/r.php?loc=bottom&refid=8')
		self.browser.find_by_name('firstname').last.fill(self.first_name)
		self.browser.find_by_name('lastname').last.fill(self.last_name)
		self.browser.find_by_name('email').last.fill(self.email)
		
		if self.gender==u'MALE':
			self.browser.find_by_id('gender').last.select('2')
			
		if self.gender==u'FEMALE':
			self.browser.find_by_id('gender').last.select('1')
			
		self.browser.find_by_id('day').last.fill(self.BirthDay)
		self.browser.find_by_id('month').last.fill(self.BirthMonth)
		self.browser.find_by_id('year').last.fill(self.BirthYear)
		self.browser.find_by_name('pass').last.fill(self.password)
		
		self.browser.find_by_id('signup_button').last.click()
		self.browser.find_by_id('u_0_0').last.click()
		
		if 'checkpoint' in self.browser.url:
			val = raw_input("Inter capture: ")
			
			self.browser.find_by_id('captcha_response').last.fill(val)
			self.browser.find_by_id('u_0_0').last.click()
			
		self.browser.find_by_name('contact_point').last.fill('+7'+self.face_phone)

		self.browser.find_by_xpath('//input[@type="submit"]').click()
		
		val = raw_input("Inter Facebook SMS code: ")
		self.browser.find_by_name('pin').last.fill(val)
		self.browser.find_by_xpath('//input[@type="submit"]').click()
		self.browser.find_by_xpath('//input[@type="submit"]').click()
		self.browser.find_by_xpath('//input[@type="submit"]').click()
		self.browser.find_by_xpath('//input[@type="submit"]').click()
		
		self.facebook_profile()
	
	def facebook_profile(self):
		self.browser.visit('https://m.facebook.com/profile.php')
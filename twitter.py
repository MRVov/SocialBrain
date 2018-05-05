# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################

class twitter_brain():
	def register_twitter(self):
		self.browser.visit('https://mobile.twitter.com/signup')
		
		if self.fake_phone:
			self.twitter_phone='+7962'+self.phone
		#else:
		#	val = raw_input("Enter Twitter phone: ")
		#	self.twitter_phone=val
			
		
		self.browser.find_by_id('oauth_signup_client_fullname').last.type(self.first_last_name)
		self.browser.find_by_id('oauth_signup_client_email').last.type(self.twitter_phone)
		#self.browser.find_by_id('oauth_signup_client_screen_name').last.fill(self.login)
		self.browser.find_by_id('oauth_signup_client_screen_name').last.type(self.login)
		self.browser.find_by_id('oauth_signup_client_password').last.fill(self.password)

		#self.browser.find_by_xpath('//button[@type="submit"]').right_click()
		#self.browser.find_by_xpath('//button[@type="submit"]').right_click()
		
		
		if not self.browser.is_element_not_present_by_xpath('//div[@id="recaptcha_image"]'):
			val = raw_input("enter capture:")
		
		self.browser.find_by_xpath('//button[@type="submit"]').click()
		self.dump_to_xml()
		
		if '/welcome/interests' in self.browser.url:
			print 'All ok! quick register'
			self.profile_twitter()
			return True
		
		if '/signup/verify_phone' in self.browser.url:
			self.browser.find_by_name('phone_number').last.type(self.twitter_phone)
			
			if self.twitter_phone.find('+7')==0:
				self.browser.find_by_name('phone_country').last.select('RU')
				
			if self.twitter_phone.find('+380')==0:
				self.browser.find_by_name('phone_country').last.select('UA')
								
			self.browser.find_by_name('commit').last.click()
			
			if self.tzid:
				self.run_number()
				val=self.wait_get_sms()
			else:
				val = raw_input("Press Twitter SMS code:")
				
			self.browser.find_by_id('pin').last.fill(val)
			self.browser.find_by_id('password').last.fill(self.password)
			self.browser.find_by_name('commit').last.click()
		
		
		#self.browser.find_by_name('code').last.fill(val)
		#self.browser.find_by_xpath("//form[@action='/signup/phone/verify']//input[@name='commit']").last.click()

		#self.browser.find_by_name('email').last.fill(self.email)
		#self.browser.find_by_name('commit').last.click()
		
		#self.browser.find_by_name('settings[screen_name]').last.fill(self.login)
		#self.browser.find_by_name('commit').last.click()
		#self.browser.find_by_name('settings[password]').last.fill(self.password)
		#self.browser.find_by_name('commit').last.click()
		
		#self.profile_twitter()
		

		

	
	#self.twitter_read_account('myodoo')

	self.twitter_read_account('wwf')
	
	self.twitter_read_account('ntvru')
	self.twitter_read_account('channelone_rus')
	
	#b1.twitter_read_account('beargrylls')
	self.twitter_read_account('ru_lh')	
	self.twitter_read_account('micex_news')
	
	#self.twitter_retweet('594167830397882370')

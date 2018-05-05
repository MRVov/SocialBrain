# -*- encoding: utf-8 -*-

##############################################################################
#
#
##############################################################################

class Google_brain():
	def register_google(self):
		self.browser.visit('https://accounts.google.com/SignUp?continue=https%3A%2F%2Faccounts.google.com%2FManageAccount')
		self.browser.find_by_id('FirstName').last.fill(self.first_name)
		self.browser.find_by_id('LastName').last.fill(self.last_name)
		self.browser.find_by_id('GmailAddress').last.fill(self.login)
		
		self.browser.find_by_id('Passwd').last.fill(self.password)
		self.browser.find_by_id('PasswdAgain').last.fill(self.password)
		
		self.browser.find_by_id('BirthDay').last.select(str(int(self.BirthDay)))
		self.browser.find_by_id('BirthMonth').last.select(self.BirthMonth)
		self.browser.find_by_id('BirthYear').last.select(self.BirthYear)
		
		self.browser.find_by_id('Gender').last.select(self.gender)
		
		self.browser.find_by_id('RecoveryPhoneNumber').last.fill('+7'+self.google_phone)
		self.browser.find_by_id('RecoveryEmailAddress').last.fill(self.email)
		
		self.browser.find_by_id('SkipCaptcha').last.click()
		self.browser.find_by_id('CountryCode').last.select('RU')
		self.browser.find_by_id('TermsOfService').last.click()
		
		self.browser.find_by_id('submitbutton').last.click()
		
		if 'UserSignUpIdvChallenge' in self.browser.url:
			self.browser.find_by_name('SendCode').last.click()
			val = raw_input("Press Google SMS code:")
			self.browser.find_by_id('verify-phone-input').last.fill(val)
			self.browser.find_by_name('VerifyPhone').last.click()
			
		# Google+ Profile
		self.browser.find_by_name('gpsb').last.click()
		self.browser.find_by_name('submitbutton').last.click()
		
		self.profile_google()
		
	def profile_google(self):
		self.browser.visit('https://www.google.com/settings/general-light?hl=ru&ref=/settings/')	

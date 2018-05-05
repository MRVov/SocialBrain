# -*- encoding: utf-8 -*-

##############################################################################
#
#
##############################################################################
import sys
import os
import traceback

from splinter import Browser
sys.path.append('/home/vovan/eclipse/PaseBook')
from invents import invents
import time
import random
from lxml import etree
from tools import *

class Brain1(MegaBrainTools):
	def __init__(self, account):
		
		if account=='':
			####?
			self.gender='MALE'
			self.inn=invents()
			
			self.invent_user()
		
		#if account=='FEMALE':
		#	self.inn=invents()
		#	self.invent_user()
			
		else:
			self.account=account
			self.read_data()
			self.inn=invents()
		
		self.browser = Browser('firefox', profile_preferences=proxy_settings)
		
	def twitter_purge_about(self):
		self.browser.visit('https://mobile.twitter.com/settings/profile')
		time.sleep(3)
		self.browser.find_by_name('settings[description]').last.fill('')
		time.sleep(3)
		self.browser.find_by_name('commit').last.click()
		
	def twitter_change_login(self):
		self.browser.visit('https://mobile.twitter.com/settings/screen_name')
		self.browser.find_by_name('settings[screen_name]').last.fill(self.login)
		self.browser.find_by_name('settings[password]').last.fill(self.password)
		time.sleep(3)
		self.browser.find_by_name('commit').last.click()
		
	def twitter_login(self):
		print 'Login user %s' % self.login
		
		self.browser.visit('https://mobile.twitter.com/session/new')
		
		if hasattr(self, 'temp_pass'):
			passwd=self.temp_pass
		else:
			passwd=self.password
		login=self.twitter_phone
		
		print 'User login %s' % login
		print 'User password %s' % passwd
		
		if self.browser.url!='https://mobile.twitter.com/':
			self.browser.find_by_name('session[username_or_email]').last.fill(login)
			self.browser.find_by_name('session[password]').last.fill(passwd)
			self.browser.find_by_xpath('//button[@type="submit"]').click()
			time.sleep(5)
		
		if '/login/error?' in self.browser.url:
			print 'Error Login in Twitter for User %s' % self.login
			return False
		
		if hasattr(self, 'temp_pass'):
			print self.login
			print self.temp_pass
			print self.password
			
			self.browser.visit('https://mobile.twitter.com/settings/password')
			
			self.browser.find_by_name('settings[current_password]').last.fill(self.temp_pass)
			time.sleep(3)
			self.browser.find_by_name('settings[password]').last.fill(self.password)
			time.sleep(3)
			self.browser.find_by_name('settings[password_confirmation]').last.fill(self.password)
			time.sleep(3)
			self.browser.find_by_name('commit').last.click()
			time.sleep(5)
			print 'First login for account %s done. Save to storage' % self.login
			
			del self.temp_pass
			self.dump_to_xml()
			
			self.twitter_login()
			self.twitter_change_login()
			
			self.twitter_profile()
		return True

	def twitter_logout(self):
		self.browser.visit('https://mobile.twitter.com/account')
		self.browser.find_by_xpath('//input[@value="Log out"]').click()
		
	def twitter_compose(self, mess):

		self.browser.visit('https://mobile.twitter.com/compose/tweet')
		self.browser.find_by_name('//textarea[@class="tweet-box-textarea userselect"]').last.fill(mess)
		self.browser.find_by_xpath('//a[@class="tweet-button button disabled"]').click()
		
	def twitter_read_account(self, account):

		print 'https://twitter.com/%s' % account
		self.browser.visit('https://twitter.com/%s' % account)
		button=self.browser.find_by_xpath('//button[@class="user-actions-follow-button js-follow-btn follow-button btn"]')
		
		if button.text in ['Follow', u'Читать']:
			button.click()
		else:
			print 'May be already read Unwrong button value- %s' % button.text
				
		time.sleep(5)
		
	def twitter_stop(self):
		val = raw_input("Stop Was Here")
		
	def twitter_check(self):
		pass
					
	def twitter_retweet(self, mess_id):
		
		self.browser.visit('https://mobile.twitter.com/statuses/%s/retweet' % mess_id)
		
		if not self.browser.is_element_not_present_by_xpath("//form[@action='/statuses/%s/retweet']//input[@name='commit']" %  mess_id):
			self.browser.find_by_xpath("//form[@action='/statuses/%s/retweet']//input[@name='commit']" %  mess_id).last.click()
		else:
			print 'Element for read don found. May be already retweet'
			
	def twitter_profile(self):
		print self.photo_path
		
		if not os.path.exists(self.photo_path):
			print 'Error get file %s' % self.photo_path
			
		self.browser.visit('https://twitter.com/%s' % self.login)
		self.browser.find_by_xpath("//button[contains(@class,'UserActions-editButton edit-button btn')]").click()
		time.sleep(1)
		
		self.browser.find_by_xpath(xpath='//div[@class="ProfileCanopy-avatar"]//button[@class="ProfileAvatarEditing-button u-boxShadowInsetUserColorHover"]').click()
		time.sleep(1)
		self.browser.attach_file('media[]', self.photo_path)
		time.sleep(1)

		self.browser.find_by_xpath(xpath='//div[@id="profile_image_upload_dialog"]//button[@class="btn primary-btn profile-image-save"]').click()
		time.sleep(1)
			
		#self.browser.find_by_xpath(xpath='//div[@class="Grid-cell"]//button[@id="js-userColorButton"]').click()
		#colours=['0000FF','2E2B57','008b45','ff0000','6633FF','3300CC','3300FF','6600CC','006633','FF6600']
		#self.browser.find_by_xpath(xpath='//div[@class="ColorPicker dropdown-menu"]//input[@class="ColorPicker-hexInput"]').fill(random.choice(colours))
		
		self.browser.visit('https://mobile.twitter.com/settings/profile')
		time.sleep(3)
		self.browser.find_by_name('settings[fullname]').last.fill(self.first_last_name)
		time.sleep(3)
		self.browser.find_by_name('settings[location]').last.fill(self.city)
		time.sleep(3)
		#self.browser.find_by_name('settings[description]').last.fill(self.inn.get_citation())
	
		self.browser.find_by_name('commit').last.click()	
		
		self.browser.visit('https://mobile.twitter.com/settings/email')
		time.sleep(3)
		self.browser.find_by_name('settings[email]').last.fill(self.email)
		time.sleep(3)
		self.browser.find_by_name('settings[password]').last.fill(self.password)
		time.sleep(3)
		#self.browser.find_by_name('settings[description]').last.fill(self.inn.get_citation())
	
		self.browser.find_by_name('commit').last.click()			
if __name__ == '__main__':

	tree = etree.parse(file_path)
	root=tree.getroot()
				
	def procc_task(task):
		network=task[1].split('_')[0]
		
		function=task[1]
		params=task[2:]
		login=task[0]
		
		b1=Brain1(login)
		
		log_res=False
		if network=='twitter':
			log_res=b1.twitter_login()
		
		if not log_res:
			print 'Error login for EXE task %s for login %s SKIPED' %  (function, login)
			b1.browser.quit()
			return False
		try:
			method = getattr(b1, function)
			method(*params)
		except:
			print(traceback.format_exc())
			print(sys.exc_info()[0])
			print "Ошибка", sys.exc_info()[0]
			
		b1.browser.quit()

	def gobotronic_task(task):
		print 'Start Gobotronic Task'
		network=task[1].split('_')[0]
		print 'Network %s' % network
		
		task[0]=task[0]
		
		xpath="//%s_phone[text() != \'*\']" % network
		x_arr=root.xpath(xpath)
					
		if task[0].lower()=='all':	

			print 'Total accounts in Twitter %d' % len(x_arr)
			
			for br in x_arr:
				phone = etree.SubElement(br, "%s_phone" % network)
				
				br_task=task
				br_task[0]=br.getparent().get("login")
				procc_task(br_task)
				
		elif task[0].lower()=='random':
			
			br=random.choice(x_arr)
			br_task=task
			br_task[0]=br.getparent().get("login")
			
			print 'Random user %s' % br_task[0]
			
			procc_task(br_task)
		else:
			procc_task(task)
				
		print 'End Gobotronic Task'
		
	def filetronic(order_id, network):
		with open(os.getcwd()+'/order_%s.txt' % order_id, "r") as ins:
			for line in ins:
				srt_arr=line.split(';')
	
				phone_number='+'+srt_arr[4].replace('\r\n', '')
				temp_pass=srt_arr[1]
				
				print phone_number
				print temp_pass
				
				b1=Brain1('')
				b1.twitter_phone=phone_number
				b1.temp_pass=temp_pass
				
				method = getattr(b1, '%s_login' % network)
				method()
				#return True
	
	def clean_dead():
		xpath="//Item[./twitter_phone/text()=\'*\' and ./vk_phone/text()=\'*\' and ./google_phone/text()=\'*\' and ./face_phone/text()=\'*\']"
		x_arr=root.xpath(xpath)
		for br in x_arr:
			print br.get("login")
			root.remove(br)

		et = etree.ElementTree(root)
		et.write(file_path, pretty_print=True, encoding="UTF-8")
		

	gobotronic_task(['AleksaKul63','twitter_stop'])
	
	
	#End Gobotronic Task

	#b1=Brain1('')
	#b1.register_twitter()
	
	#b1=Brain1('romasazonov33')
	#b1.twitter_login()
	#b1.profile_twitter()
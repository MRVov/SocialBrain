# -*- encoding: utf-8 -*-

##############################################################################
#
#
##############################################################################
import sys
import os
import traceback
import base64
from splinter import Browser
sys.path.append('/home/vovan/eclipse/PaseBook')
from invents import invents
import time
import random
from lxml import etree
from tools import *

import getpass, imaplib
import email
from lxml import etree
import lxml.html

domain='p312429.for-test-only.ru'
antigate_key='ekey'

def recognize_captcha(url, cook=None):
	try_count=6
	wait_sec=7
	
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0',
			'Cookie': cook,
			}

	req = urllib2.Request(url)
	req.add_header("Cookie", cook) # передаём cookie
	f = urllib2.urlopen(req)

	#data = f.read()
	#print headers
	#f = urllib.urlopen(url, None, headers )
	#print f.info()
	image=f.read()
	
	

	param={
		'method':'base64',
		'is_russian':'0',
		'key':antigate_key,
		'body':base64.b64encode(image)
		}
	
	host='http://antigate.com/in.php'
	param=urllib.urlencode(param)
	
	cap_req = urllib.urlopen(host, param, headers)
	#cap_req.info()
	body = cap_req.read().split('|')
	
	captcha_id=0
	
	if len(body) == 2:
		captcha_id = int(body[1])
	else:
		print 'Error antigate state- %s' % body
		return -1

	for i in range(try_count):
		check_url='http://antigate.com/res.php?key=%s&action=get&id=%d' % (antigate_key, captcha_id)
		f = urllib.urlopen(check_url, None, headers)

		check_body=f.read()
		if check_body[:3]=='OK|':return check_body[3:]
		time.sleep(wait_sec-i)
		
	return 'NO WOIT MORE'

class Brain5(MegaBrainTools):
	def __init__(self):
		pass
	
	def get_email_confirm(self, email_name, email_domain, robot_name, xpath):
		print 'Start Email confirm'
		print email_name, email_domain, robot_name, xpath
		try_count=80
		wait_time=15
		
		pdd_host='imap.yandex.ru'
		pdd_user='all@mail.sru'
		pdd_pass='@$%&IrKr*01'
		
		pdd_host='p3124s9.mail.ihc.ru'
		pdd_user='admin@p31242c.for-test-only.ru'
		pdd_pass='7Ur3hVm7c'
		

		#http://www.travelingfrontiers.com/projects/doku.php?id=imapv4_protocol
	
		for i in range(try_count):
			print 'Total wait', (i-1)*wait_time
			M = imaplib.IMAP4_SSL(pdd_host)
			M.login(pdd_user, pdd_pass)
			M.select()
			print 'End init'
		
			#typ, data = M.search(None, '(HEADER TO "<%s@%s>" FROM "%s")' % (email_name, email_domain, robot_name))
			#typ, data = M.search(None, '(FROM "%s")' % ( robot_name))
			#print '(TO "<%s@%s>" )' % (email_name, email_domain)
			typ, data = M.search(None, '(TO "%s@%s" FROM "%s")' % (email_name, email_domain, robot_name))
			print typ, data
			
			if data[0]!='':
				ids_arr=data[0].split()
				
				for mess_id in ids_arr:
			
					typ, body=M.fetch(mess_id, '(RFC822)')
					
					msg = email.message_from_string(body[0][1])
		
					for part in msg.walk():	   
						if part.get_content_type() == "text/html":
							body = part.get_payload(decode=True)
							html = lxml.html.fromstring(body)
							r = html.xpath(xpath)
							if len(r)>0: 
		 						return r[0].get("href")
	 						else:
	 							print 'Xpath donf found in mail SKIP'
		 			print 'Dont found html context- Exit'
		 			
			time.sleep(wait_time)
			
			M.close()
			M.logout()	
		
	def freelance_register(self, ref='myodooru'):
		self.inn=invents()
		self.inn.lang='ENG'
		self.inn.generate()
		
		self.name=self.inn.FirstName+' '+self.inn.LastName
		self.password=self.inn.generate_pass()
		self.login=self.inn.generate_email()
		
		self.email=self.login+'@'+domain
		
		print self.login
		
		self.browser = Browser('firefox', profile_preferences=proxy_settings)
		self.browser.visit('https://www.freelancer.com/affiliates/%s' % ref)
		self.browser.find_by_id('sign-up').first.click()
		
		self.browser.find_by_name('email').last.fill(self.email)
		self.browser.find_by_name('newusername').last.fill(self.login)
		self.browser.find_by_name('newuserpasswd').last.fill(self.password)
		self.browser.find_by_name('newuserpasswd1').last.fill(self.password)
		
		self.browser.find_by_id('looking_to_hire').first.click()
		self.browser.find_by_xpath('//fieldset//button[@type="submit"]').first.click()
		time.sleep(15)
		
		if 'www.freelancer.com/users/onsignup.php' in self.browser.url:
			print 'We are cathed!'
			url=self.browser.find_by_id('recaptcha_challenge_image').first['src']
			cap=recognize_captcha(url)
			self.browser.find_by_id('recaptcha_response_field').last.fill(cap)
			self.browser.find_by_xpath('//input[@type="submit"]').first.click()
			time.sleep(5)
			
		if 'www.freelancer.com/users/i_am_human.php' in self.browser.url:
			print 'BAD induce'
			url=self.browser.find_by_id('recaptcha_challenge_image').first['src']
			cap=recognize_captcha(url)
			self.browser.find_by_id('recaptcha_response_field').last.fill(cap)
			self.browser.find_by_xpath('//input[@type="submit"]').first.click()
			time.sleep(5)
			
		if 'www.freelancer.com/users/i_am_human.php' in self.browser.url:
			print 'BAD induce'
			url=self.browser.find_by_id('recaptcha_challenge_image').first['src']
			cap=recognize_captcha(url)
			self.browser.find_by_id('recaptcha_response_field').last.fill(cap)
			self.browser.find_by_xpath('//input[@type="submit"]').first.click()
			time.sleep(5)
			
		self.dump_to_xml(tree_name='ItemFreeLance')
		
		link=self.get_email_confirm(self.login, domain, 'noreply@freelancer.com', "//a[contains(@href,'www.freelancer.com/users/onverify.php?')]")
		print 'Activation link=', link
		
		self.browser.visit(link)
		time.sleep(10)
		
		
	def freelance_register_old(self, id=1):
		work_name='Modify Python scripts'
		#work_name='Web application based python'
		#work_name='Choosing hosting service and installing Odoo'
		
		brif='Contact me for more information.'
		#Recommended
		
		#self.browser.visit('http://kurufin.ru/html/Name_generator/random_name_english.html')
		#self.browser.find_by_name('generate').last.click()
		
		#self.inn.FirstName= self.browser.find_by_name('first').last.value.strip()
		#self.inn.LastName=self.browser.find_by_name('last').last.value.strip()
		
		#print self.inn.FirstName
		
		self.name=self.inn.FirstName+' '+self.inn.LastName
		self.password=self.inn.generate_pass()
		self.login=self.inn.generate_email()
		
		
		self.email=self.login+'@mail.ru'

		
		self.browser.visit('https://www.freelancer.com/affiliates/trokbrok')
		self.browser.find_by_xpath('//a[@data-action="hire-section"]').first.click()
		self.browser.select('skill_category', '1')
		self.browser.select('skill_subcategory', '4')
		self.browser.find_by_id('post-project-bt').first.click()
		
		time.sleep(10)
		
		self.browser.find_by_name('email').last.fill(self.email)
		self.browser.find_by_name('newusername').last.fill(self.login)
		self.browser.find_by_name('newuserpasswd').last.fill(self.password)
		self.browser.find_by_name('newuserpasswd1').last.fill(self.password)
		
		self.browser.find_by_name('project_name').last.fill(work_name)
		self.browser.find_by_name('description').last.fill(brif)
		
		self.browser.find_by_id('post-project-submit').first.click()
		
		self.dump_to_xml(tree_name='ItemFreeLance')
		time.sleep(15)
		self.browser.visit('https://www.freelancer.com/u/trokbrok.html')
		time.sleep(3)
		
	def freelance_login(self):
		self.browser.visit('https://www.freelancer.com/')
		
		self.browser.find_by_id('login-normal').first.click()
		
		self.browser.find_by_name('username').last.fill(self.login)
		self.browser.find_by_name('passwd').last.fill(self.password)
		
		self.browser.find_by_id('login-bt').first.click()
		time.sleep(10)
		
	def freelance_copy_project(self):
		self.browser.visit('https://www.freelancer.com/jobs/Python/1/')
		time.sleep(10)

		self.browser.find_by_xpath('//li[@class="control-group language twocol"]//a[@class="select2-search-choice-close fl-icon-close"]').first.click()
		time.sleep(10)

		links_arr=self.browser.find_by_xpath("//a[contains(@href,'https://www.freelancer.com/projects/')]")
		
		random.choice(links_arr).click()
		time.sleep(10)

		self.browser.find_by_xpath('//a[@class="btn btn-large btn-primary align-c margin-t10 repostProjectButton"]').click()
		time.sleep(10)

		if 'freelancer.com/payments/verify.php?' in self.browser.url:
			print 'We are cathed!'
			return False
					
		self.browser.find_by_id('formSubmit').first.click()
		time.sleep(10)

		if '/buyers/project-upgrades.php?' in self.browser.url:
			self.browser.find_by_id('btn_submit_id_no_upgrade').first.click()
			
		time.sleep(10)
		project_url=self.browser.url.split('?')[0]
		
		self.browser.quit()
		return project_url
		#
		
	def freelance_bid_project(self, project_url, val=2000):
		self.browser.visit(project_url)
		self.browser.find_by_xpath('//a[@class="btn btn-primary btn-large bidButton"]').first.click()
		time.sleep(10)
		self.browser.find_by_name('sum').first.fill(str(val))
		self.browser.find_by_id('place-bid').first.click()
		
	def freelance_split_project(self, project_url, project_value=2000):
		time.sleep(10)
		#self.browser.visit(project_url+'#placebid')
		#time.sleep(10)
		#self.browser.find_by_xpath('//a[@class="margin-r10 editBid"]').first.click()
		
		self.browser.find_by_name('descr').last.fill('All we be done sheaf '*30)
		
		
		stoune_len=6
		
		print range (1, stoune_len+1)
		
		for i in range (1, stoune_len+1):
			if i==stoune_len:
				val=project_value-((project_value/stoune_len)*stoune_len)+project_value/stoune_len
			else:
				val=project_value/stoune_len
				
			print i
			print val
			self.browser.find_by_id('add-milestone-proposal').first.click()
			self.browser.find_by_name('milestone-descr-%d' % i).first.fill('All we be done sheaf ')
			self.browser.find_by_name('milestone-amount-%d' % i).first.fill(str(val))
		
		self.browser.find_by_id('place-bid').first.click()
				
	def main_init(self):
		self.read_data( tree_name='Item')
		self.browser = Browser('firefox', profile_preferences=proxy_settings)
		self.freelance_login()	
			
	def freelance_brain1(self):
		#self.account="eduardsoko40"
		#self.main_init()
		#project_url=self.freelance_copy_project()
		
		#print project_url
		
		self.account="myodoo"
		self.main_init()
		project_url='https://www.freelancer.com/jobs/php/Setup-VOIP-Solution-Using-Oktell-7706859/																																																																																																																																																																																																								 '
		#self.freelance_bid_project(project_url)
		#self.freelance_split_project(project_url)
		

	
		
fl=Brain5()
count=0

while True:
	count=count+1
	print count

	#fl.freelance_register(ref='johntrace49')	
	try:
		fl.freelance_register()
	except:
		pass
	fl.browser.quit()
	
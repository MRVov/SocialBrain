# -*- encoding: utf-8 -*-

##############################################################################
#
##############################################################################
import requests
import time

class sms():
	def wait_register_number(id):
		for i in range(300):	
			r = requests.get('http://api.sms-reg.com/getState.php?tzid=%s&apikey=sekret' % id)
			res=r.json()
			print res
			if res['response']=='TZ_NUM_PREPARE':
				return res['number']
			
			if res['response']=='WARNING_NO_NUMS':
				print 'Not FREE numbers'
				return False
			time.sleep(5)
			
		return False
	
	def wait_get_sms(id):
		for i in range(300):	
			r = requests.get('http://api.sms-reg.com/getState.php?tzid=%s&apikey=sekret' % id)
			res=r.json()
			print res
			if res['response']=='TZ_NUM_ANSWER':
				return res['msg']
			
			time.sleep(5)
			
		return False
	
	
	def get_sms(network):
		url='http://api.sms-reg.com/getNum.php?country=ru&service=%s&apikey=sekret' % network
		r = requests.get(url)
		print r.status_code
		res=r.json()
		print res
		
		if res['response']!=u'1':
			print 'Error response status %s' % res['response'] 
			return False
		
		tzid=res['tzid']
		number=wait_register_number(tzid)
		if not number:
			print 'Error get number. All over!' 
			return False
		
		number='+'+number
		print number
		
		b1=Brain1('')
		b1.twitter_phone=number
		b1.tzid=tzid
		b1.register_twitter()
		
		r = requests.get('http://api.sms-reg.com/setReady.php?tzid=%s&apikey=sekret' % tzid)
		res=r.json()
		if res['response']!=u'1':
			print 'Error response status %s' % res['response']
			return False
		
		sms_code=wait_get_sms(tzid)
		if not sms_code:
			print 'Error get SMS. All over! '
			return False
	def run_number(self):
		r = requests.get('http://api.sms-reg.com/setReady.php?tzid=%s&apikey=sekret' % self.tzid)
		res=r.json()
		if res['response']!=u'1':
			print 'Error response status %s' % res['response']
			return False
			
	def wait_get_sms(self):
		for i in range(300):	
			r = requests.get('http://api.sms-reg.com/getState.php?tzid=%s&apikey=sekret' % self.tzid)
			res=r.json()
			print res
			if res['response']=='TZ_NUM_ANSWER':
				return res['msg']
			
			time.sleep(5)
			
		return False
# -*- encoding: utf-8 -*-

##############################################################################
#
#  Autor Dementiev Sergey
#  sde@arterp.ru
#  www.arterp.ru
#
##############################################################################
import sys
import os
from splinter import Browser
sys.path.append('/home/vovan/eclipse/PaseBook')
from invents import invents
import time
import random
from lxml import etree
import json
import requests
import urllib2
import urllib
from urllib import urlencode
from urllib2 import URLError

file_path=os.getcwd()+'/storage.xml'

proxy_settings2 = {'network.proxy.type': 1,
	   'network.proxy.socks': 'localhost',
	   'network.proxy.socks_port': 8080,
	   #'network.proxy.socks': '178.124.70.241',
	   #'network.proxy.socks_port': 1080,	   
	   
	    'network.proxy.socks_version': 4, 
	    
	   #'network.proxy.http': '5.9.190.133',
	   #'network.proxy.http_port': 8080,
	   	   
	   
	   'network.proxy.no_proxies_on':'',
	   #'general.useragent.override':'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+'
	   						}
proxy_settings = {}
class MegaBrainTools():

	def invent_user(self):
		#self.gender=gender
		
		#self.gender=u'FEMALE'
		
		if self.gender=='MALE':
			self.inn.generate(is_male=True)
			
		if self.gender=='FEMALE':
			self.inn.generate(is_male=False)
			
		self.password=self.inn.generate_pass()
		self.login=self.inn.generate_email()

		self.first_name=self.inn.FirstName
		self.last_name=self.inn.LastName
		
		self.first_last_name=self.first_name +u' '+ self.last_name
		self.email=self.login+u'@arterp.ru'
		
		self.city=self.inn.generate_city()
		
		self.phone=str(self.inn.phone)

		self.work=self.inn.generate_work()
		
		self.BirthDay=self.inn.BirthDay
		self.BirthMonth=self.inn.BirthMonth
		self.BirthYear=self.inn.BirthYear
		
		self.twitter_phone='*'
		self.google_phone='*'
		self.face_phone='*'
		self.vk_phone='*'
		self.get_photo_path()
		self.dump_to_xml()
		
	def get_photo_path(self):	
		#return self.login
		if self.gender=='MALE':
			self.photo_path=u'/home/vovan/PhotoS/boys/'
			
		if self.gender=='FEMALE':
			self.photo_path=u'/home/vovan/PhotoS/girls/'
			
		ret_arr=[]	
		for fil in os.listdir(self.photo_path):
			ret_arr.append(os.path.basename(fil))
			
		self.photo_path=self.photo_path+random.choice(ret_arr)
		
		tree = etree.parse(file_path)
		root=tree.getroot()
		
		if len(root.xpath("//Item[@photo_path=\'%s\']" % self.photo_path))!=0:
			self.get_photo_path()
			
	def dump_to_xml(self, tree_name='Item'):
		
		tree = etree.parse(file_path)
		root=tree.getroot()
		
		for bad in root.xpath("//%s[@login=\'%s\']" % (tree_name, self.login)):
			bad.getparent().remove(bad)  	
			
		item_branch= etree.Element("Item", login=self.login)		
		for curr in self.__dict__:
			elem=etree.Element(curr)
			#print self.__dict__[curr]
			elem.text=unicode(self.__dict__[curr])
			item_branch.append(elem)
		root.append(item_branch)

		xml=etree.tounicode(root, pretty_print=True)
		
		root = etree.fromstring(xml)
		et = etree.ElementTree(root)
		et.write(file_path, pretty_print=True, encoding="UTF-8")
		#print xml
		#f = open(libraryFile, 'w')
		#library.write(f, pretty_print=True)
		#f.close()
		
	def read_data(self, tree_name='Item'):
		tree = etree.parse(file_path)
		root=tree.getroot()
		
		acc=root.xpath("//%s[@login=\'%s\']" % (tree_name, self.account))
		if len(acc)>0:
			my_item=root.xpath("//Item[@login=\'%s\']" % self.account)[0]
		else:
			raise NameError('Login %s don\'t found' % self.account)
		
		for curr in my_item:
			setattr(self, curr.tag, unicode(curr.text))
import sqlite3
import urllib
import urllib2
#'E:\Dev\Database\okc-full.db'


class OKCupidDataWriter:
	def __init__(self,database):
		self.conn = sqlite3.connect(database)
		self.cursor = conn.cursor()

class OKCupidNavigator:
	def __init__(self):


	def LoginToOkCupid(self,username, password):
		url= 'http://www.okcupid.com/login'
		user=urllib.urlencode(
				{'username':username,
				 'password':password})
		req = urllib2.Request(url,user)
		urlOpener.open(req)
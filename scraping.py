from HTMLParser import HTMLParser
from _sqlite3 import IntegrityError
import cookielib
import urllib
import urllib2
import ast
import re
import web
import time
import sys
import sqlite3
import lxml
__author__ = 'David'

from BeautifulSoup import BeautifulSoup
#http://axiomofcats.com/2012/07/30/data-mining-okcupid/
#Log in
cj = cookielib.CookieJar()

opener = urllib2.build_opener(
	urllib2.HTTPCookieProcessor(cj),
	urllib2.HTTPRedirectHandler,
	urllib2.ProxyHandler({"http":"http://14.139.233.70:8080"})
)


opener.addheaders.append(('User-agent','Mozilla/4.0'))

url= 'http://www.okcupid.com/login'
user1=urllib.urlencode(
		{'username':'JosephIss',
		 'password':'J053ph!SS'})
user2=urllib.urlencode(
		{'username':'CompSciChi',
		 'password':'Cloverx123'})
login_data=user1

req = urllib2.Request(url,login_data)

resp = opener.open(req)
#Logged in

web.config.debug=False
db = web.database(dbn='sqlite',db='database/OKC_users.db')
#Search
conn = sqlite3.connect('E:\Dev\Database\okc-full.db')
cursor = conn.cursor()
searchAge=18

while searchAge<100:
	#online this month
	#url = "http://www.okcupid.com/match?filter1=0%2C34&filter2=2%2C{0}%2C{0}&filter3=3%2C25&filter4=5%2C2678400&filter5=1%2C1&filter6=35%2C0&locid=0&timekey=1368602393&matchOrderBy=SPECIAL_BLEND&custom_search=0&fromWhoOnline=0&mygender=m&update_prefs=1&sort_type=0&sa=1&using_saved_search=&low=1&count=1000&ajax_load=1".format(searcgAge)
	#online this year
	url = "http://www.okcupid.com/match?filter1=0%2C34&filter2=2%2C{0}%2C{0}&filter3=3%2C25&filter4=5%2C31536000&filter5=1%2C1&filter6=35%2C0&locid=0&timekey=1368683277&matchOrderBy=SPECIAL_BLEND&custom_search=0&fromWhoOnline=0&mygender=m&update_prefs=1&sort_type=0&sa=1&using_saved_search=&low=1&count=1000&ajax_load=1".format(searchAge)
	searchAge += 1
	dupes=0
	lastRowCount=0
	rowCount=1
	while rowCount>lastRowCount:
		lastRowCount =rowCount
		cursor.execute("SELECT count(*) FROM Users")
		rowCount =cursor.fetchone()[0]

		req=urllib2.Request(url)
		resp=opener.open(req)
		json = resp.read()
		html = ast.literal_eval(json)['html']
		soup = BeautifulSoup(html)
		usernames = soup.findAll(attrs={"class":"username"})
		asos = soup.findAll(attrs={"class":"aso"})
		locations = soup.findAll(attrs={"class":"location"})
		for i in range(0,len(usernames)):
			username = usernames[i].text
			aso = asos[i].text
			matchobj = re.match(r"^(\d+).*(F|M).*(Bi|Straight).*/.*;(.*)",aso)
			age = matchobj.group(1)
			sex = matchobj.group(2)
			orientation = matchobj.group(3)
			status = matchobj.group(4)
			location = locations[i].text
			insert_sql = "INSERT INTO Users VALUES ('%(user)s','%(age)s','%(sex)s','%(orientation)s','%(status)s','%(location)s')"%{'user':username,'age':age,'sex':sex,'orientation':orientation,'status':status,'location':location}
			try:
				print insert_sql
				cursor.execute(insert_sql)
				conn.commit()
			except IntegrityError:
				dupes += 1
				print "%i duplicates"%dupes
		time.sleep(30) #don't kill the servers
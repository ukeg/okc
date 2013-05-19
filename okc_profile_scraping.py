from _sqlite3 import IntegrityError
import cookielib
import sqlite3
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import time
import web



def test():
	opener = InitializeOpener()
	cursor = InitializeDataCursor()
	LoginToOkCupid('JosephIss','J053ph!SS',opener)
	profileUrl = 'http://www.okcupid.com/profile/zwigglez'
	req=urllib2.Request(profileUrl)
	resp = opener.open(req)
	html = resp.read()
	print html



def main():
	opener = InitializeOpener()
	cursor = InitializeDataCursor()
	LoginToOkCupid('JosephIss','J053ph!SS',opener)
	StartScraping(cursor,opener)

def StartScraping(cursor, opener):
	usernames = GetUserNames(cursor)
	for username in usernames:
		try:
			print username
			Scrape(username,opener,cursor)
			#time.sleep(3) #don't kill the servers
		except Exception as e:
			print '%s failed for some reason...'%username


def Scrape(username,opener,cursor):
	profileUrl = 'http://www.okcupid.com/profile/{0}'.format(username)
	req=urllib2.Request(profileUrl)
	resp = opener.open(req)
	html = resp.read()
	soup =  BeautifulSoup(html)
	titles = soup.findAll(attrs={"class": "essay_title"})
	essays = soup.findAll(attrs={"id": lambda val:val and val.startswith("essay_text_")})
	gentation = SafeText(soup.find(id="ajax_gentation"))
	lookingfor = SafeText(soup.find(id="ajax_lookingfor"))
	ages = SafeText(soup.find(id="ajax_ages"))
	near = SafeText(soup.find(id="ajax_near"))
	single = SafeText(soup.find(id="ajax_single"))
	last_online = SafeText(soup.find(id="ajax_fancydate"))#broken - attribute class facnydate
	ethnicity = SafeText(soup.find(id="ajax_ethnicities"))
	height = SafeText(soup.find(id="ajax_height"))
	body_type = SafeText(soup.find(id="ajax_bodytype"))
	diet = SafeText(soup.find(id="ajax_diet"))
	smokes = SafeText(soup.find(id="ajax_smoking"))
	drinks = SafeText(soup.find(id="ajax_drinking"))
	drugs = SafeText(soup.find(id="ajax_drugs"))
	religion = SafeText(soup.find(id="ajax_religion"))
	sign =  SafeText(soup.find(id="ajax_sign"))
	education = SafeText(soup.find(id="ajax_education"))
	job = SafeText(soup.find(id="ajax_job"))
	income = SafeText(soup.find(id="ajax_income"))
	offspring = SafeText(soup.find(id="ajax_children"))
	pets = SafeText(soup.find(id="ajax_pets"))
	speaks =SafeText(soup.find(id="ajax_languages"))

	for title in titles:
		if title.text.find("looking for")>-1:
			titles.remove(title)

	for i in range(0,len(titles)):
		title = titles[i].text
		essay = essays[i].text
		essay=essay.replace('"','\'')

		insert_sql = """INSERT INTO UserEssays VALUES ("%(username)s","%(title)s","%(essay)s")"""%{'username':username,'title':title,'essay':essay}
		try:
			cursor.execute(insert_sql)
		except IntegrityError:
			pass

	insert_sql = """INSERT INTO UserAttributes VALUES ("%(drugs)s","%(username)s","%(gentation)s","%(lookingfor)s","%(ages)s","%(near)s","%(single)s","%(last_online)s","%(ethnicity)s","%(height)s","%(body_type)s","%(diet)s","%(smokes)s","%(drinks)s","%(religion)s","%(sign)s","%(education)s","%(job)s","%(income)s","%(offspring)s","%(pets)s","%(speaks)s")"""\
	%{'username':username,'gentation':gentation,'lookingfor':lookingfor,'ages':ages,'near':near,'single':single,
																	  'last_online':last_online,'ethnicity':ethnicity,'height':height,'body_type':body_type,'diet':diet,'smokes':smokes,'drinks':drinks,
																	  'drugs':drugs,'religion':religion,'sign':sign,'education':education,'job':job,'income':income,'offspring':offspring,'pets':pets,'speaks':speaks}
	insert_sql = insert_sql.replace("&ndash;","-").replace("&mdash;","-").replace("&rsquo;","\'").replace("&prime;",'\'').replace("&Prime;",'\'')
	try:
		cursor.execute(insert_sql)
	except IntegrityError:
		pass
	conn.commit()

def SafeText(soupElement):
	if soupElement:
		return soupElement.text
	return ''

def GetUserNames(cursor):
	cursor.execute("SELECT Username FROM Users WHERE NOT EXISTS (SELECT 1 FROM UserAttributes WHERE Users.Username = UserAttributes.Username )")
	usernames = cursor.fetchall()
	return [item for usernames[0] in usernames for item in usernames[0]]

def InitializeOpener():
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(
		urllib2.HTTPCookieProcessor(cj),
		urllib2.HTTPRedirectHandler,
		#urllib2.ProxyHandler({"http":"http://184.154.158.227:80"})
		#urllib2.ProxyHandler({"http":"http://221.130.162.51:81"})
		urllib2.ProxyHandler({"http":"http://58.23.3.190:810"})
	)
	urllib2.install_opener(opener)
	opener.addheaders.append(('User-agent','Mozilla/4.0'))
	web.config.debug=False
	return opener



conn = sqlite3.connect('E:\Dev\Database\okc-full.db')
def InitializeDataCursor():
	cursor = conn.cursor()
	return cursor





def LoginToOkCupid(username, password,urlOpener):
	url= 'http://www.okcupid.com/login'
	user=urllib.urlencode(
		{'username':username,
		 'password':password})
	req = urllib2.Request(url,user)
	urlOpener.open(req)


main()
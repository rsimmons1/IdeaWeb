import time
import urllib2
import requests
# from urllib3 import HTTPConnectionPool
import httplib
import json
info = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=links&format=json&pllimit=max&titles=physics').json()
thing = info['query']['pages']['22939']['links']
search = []
for s in thing:
	search.append(s['title'].encode('ascii',errors='ignore'))

from pymongo import MongoClient
def connect(dbName,colName,website=None,port=None):
	client = MongoClient(website,port)
	db = client[dbName]
	return db[colName]

def timer(func,var):
	time1 = time.time()
	func(*var)
	time2 = time.time()
	print str(func.__name__)+" : "+str(time2 - time1)

def urlConnect(words):
	for word in words:
		req = urllib2.Request('https://en.wikipedia.org/wiki/'+word)
		response = urllib2.urlopen(req)
		the_page = response.read()

def apiConnect(words):
	for word in words:
		requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&rvprop=content&titles='+word).json()

def httpConnect(words):
	conn = httplib.HTTPSConnection("en.wikipedia.org")
	articles = {}	
	for word in words:
		conn.request("GET", '/w/api.php?action=query&prop=extracts&format=json&rvprop=content&titles='+word)
		r1 = conn.getresponse()
		info = json.loads(r1.read())
		info['query']

search = ['Apple','Tree','Genus','Plant','Aristotle','Physics','Force','Velocity','Kinematics','Robotics']
print len(search)
# timer(urlConnect,search)
# timer(apiConnect,search)
# timer(httpConnect,search)




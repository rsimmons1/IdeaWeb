import json
import requests
import commonwords
import time
import Connect
import sys
import httplib
import random
collection = Connect.connect('wikiGraph','articleNodesTest','104.131.67.157',40000)
def connArticle(word):
		url2 = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts|links&format=json&explaintext=&pllimit=max&titles='+word+'&redirects='
		r = requests.get(url2)
		r2 = r.json()
		info = {}
		data = r2['query']['pages']
		Tkey = data.keys()
		article = data[Tkey[0]]
		return article
	
def generateNode(article,status='single'):
	t1 = time.time()
	if status == 'single':
		url2 = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts|links&format=json&explaintext=&pllimit=max&titles='+article+'&redirects='
		r = requests.get(url2)
		r2 = r.json()
		data = r2['query']['pages']
		datum = r2['query']
	else:
		data = article['query']['pages']
		datum = article['query']
	
	Tkey = data.keys()
	name = data[Tkey[0]]['title']
	t2 = time.time()
	finalNode = {}
	if(Tkey[0] == "-1"):##Error Handling
		print "noLink "+name
		return finalNode
	
	fullNames = []
	shortWords = []
	
	info2 = data[Tkey[0]]['extract'].split("References")[0].replace('\\', " ")

	info2 = info2.lower()
	info2 = info2.encode('ascii',errors='ignore')
	links = getLinks(name,data)
	infoArray = info2.split()
	sortedLinks = []
	wordScore = 0
	finalNode['title'] = name
	finalNode['save'] = [name.upper()]
	if 'redirects' in datum:
		finalNode['save'].append(datum['redirects'][0]['from'].upper())
	finalNode['edges'] = []
	finalNode['scanned'] = False
	connectionNum = 5
	for key in links['partial']:
		links['partial'][key] += infoArray.count(key.lower())
	for key in links['partial']:
		sortedLinks.append([key,links['partial'][key]])
	sortedLinks.sort(key = lambda x: x[1],reverse=True)
	if (len(sortedLinks) < connectionNum):
		return {}
	else:
		for x in range(connectionNum):
			finalNode['edges'].append(sortedLinks[x][0])
	time5 = time.time()
	for item in sortedLinks:
		shortWords = []
		for link in links['full'].keys():
			if(item[0].lower() in link.lower()):
				wordScore = 0
				for word in link.split():
					for short in links['partial']:
						if short.lower().replace("(","").replace(")","") == word.lower().replace("(","").replace(")",""):
							wordScore += links['partial'][short]
				shortWords.append([link,wordScore/len(link.split())])
				del links['full'][link]
		# if len(fullNames) > 4:
		# 	break
		if bool(shortWords):
			fullNames.append(max(shortWords,key=(lambda x: x[1])))
	fullNames.sort(key = lambda x: x[1],reverse=True)
	time6 = time.time()
	finalNode['edges'] = fullNames
	return finalNode

def getLinks(title,data):
	Tkey = data.keys()
	ignoreLink = ["file","image",":","category","template","\\",title.lower(),title.lower()+'s']
	ignoreWords = commonwords.words
	links = {}
	links['partial'] = {}
	links['full'] = {}
	if 'links' in data[Tkey[0]]:
		linkInfo = data[Tkey[0]]['links']
	else:
		return links
	properLink = False
	
	for item in linkInfo:
		link = item['title'].encode('ascii',errors='ignore')
		properLink = True
		for thing in ignoreLink:
			if thing in link.lower() or link.lower() in thing:
				properLink = False
				break
		if properLink:
			if not link.lower() == title.lower():
				links['full'][link] = 1
			for word in link.split():
				if not word.lower() in ignoreWords and len(word) > 1 and not word.lower() in map((lambda x: x.lower()),links['partial'].keys()):
					links['partial'][word] = 1
	return links



def find_path(graph,start, end, path=[],searches=[]):
	if searches:
		del searches[0]
	print start
	path = path + [start.lower()]
	Node = graph.find_one({'save':start.upper()})
	newpath = []
	if start.lower() == end.lower():
		return path
	if not bool(Node):
		Node = generateNode(start)
	searches += nodes['edges'][:5]
	for edge in searches:
		if not edge[0].lower() in path and not edge[0].lower() in searches:
			newpath = find_path(searches[0][0], end, path)
		if newpath: 
			return newpath
	return None

def linkHandler(articleTitles):
	conn = httplib.HTTPSConnection("en.wikipedia.org")
	articles = {}	
	articles['redirects'] = {}
	info = {}
	for word in articleTitles:
		print word+" linkHandler 1"
		url = '/w/api.php?action=query&prop=extracts|links&format=json&explaintext=&pllimit=max&titles='+word+'&redirects='
		conn.request("GET", url)
		try:
			r1 = conn.getresponse()
			info = json.loads(r1.read())
			data = info['query']['pages']
			Tkey = data.keys()
			if not info['query']['pages'].keys()[0] == "-1":
				pages = info['query']['pages']
				articles[word] = info
				if 'redirects' in info['query']:
					redirect = info['query']['redirects'][0]
					articles['redirects'][redirect['from']] = redirect['to']
		except:
			conn = httplib.HTTPSConnection("en.wikipedia.org")
	return articles

def getArticle(name,articleList):
	for word in articleList:
		if word.lower() == name.lower():
			article = articleList[word]
			article['redirects'] = []
			return articleList[word]
	
	for word in articleList['redirects']:
		if word.lower() == name.lower():
			article = articleList[articleList['redirects'][word]]
			article['redirects'] = [word.upper()]
			return article
	return None

def makeNode(initialNode,depth=None):
	searchList = []
	for query in initialNode['edges'][:depth]:
		if  not bool(collection.find_one({'save': query[0].upper()})):
			# print query[0]
			searchList.append(query[0])
	articles = linkHandler(searchList)
	print articles.keys()
	for query in articles:
			article = getArticle(query,articles)
			if 'query' in article:
				newNode = generateNode(article,'multiple')
				if(bool(newNode)):
					collection.insert_one(newNode)

def expand(counter):
	Tcount = 0
	potentials = collection.find({'scanned': False})
	number = random.randint(0,collection.find().count())
	bounce = collection.find()[number]
	print "REDIRECT "+str(bounce['title'])+" ***********************************"
	del bounce['_id']
	makeGraph(bounce,counter)


def makeGraph(initialNode,globalCount,depth=None):
	searches = []
	TNode = {}
	dbNode = {}
	for item in initialNode['edges']:
		searches.append(item)
	while bool(searches):
		item = searches[0]
		if globalCount < 1:
			return {}
		dbNode = collection.find_one({'save': item[0].upper()})
		if bool(dbNode):
			TNode = dbNode
			print TNode['save']+" "+str(TNode['scanned'])+" "+str(globalCount)+" IS ALREADY HERE!!!!"
			del TNode['_id']
		else:
			TNode = generateNode(item[0])
			print item[0]+" "+str(globalCount)+" New Connection *************"
		if(bool(TNode)):
			if not TNode['scanned']:
				makeNode(TNode,depth)
				if depth == None:
					TNode['scanned'] = True
					collection.update({'save':TNode['save']},{'$set':{'scanned':True} })
				for edge in TNode['edges'][:depth]:
					if not edge in searches:
						searches.append(edge)
				globalCount -= 1
		searches.remove(item)
		searches.sort(key=(lambda x: x[1]),reverse=True)
	expand(globalCount)




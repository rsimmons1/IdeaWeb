import json
import requests
import commonwords
import time
import Connect

collection = Connect.connect('wikiGraph','articleNodesTest')
def linkHandler(articleTitles):
	url = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts|links&format=json&explaintext=&pllimit=max&titles='+'|'.join(articleTitles)+'&redirects='
	jsonInfo = requests.get(url).json()
	articles = {}
	for item in jsonInfo['query']['pages']:
		print item
		pages = jsonInfo['query']['pages']
		title = pages[item]['title']
		articles[title] = {}
		articles[title]['article'] = pages[item]['extract']
		articles[title]['links'] = pages[item]['links']
		articles[title]['title'] = pages[item]['title']
	if 'redirects' in json['query']:
		articles['redirects'] = jsonInfo['query']['redirects']
	return articles

def getArticle(name,articleList):
	found =  False
	for item in articleList:
		if name.lower() == item.lower():
			found = True
			return articleList[item]
	if not found:
		for item in articleList['redirects']:
			if name.lower() == item['from'].lower():
				return articleList[item['to']]


def generateNode(name):
	t1 = time.time()
	url2 = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts|links&format=json&explaintext=&pllimit=max&titles='+name+'&redirects='
	r = requests.get(url2)
	r2 = r.json()
	data = r2['query']['pages']
	Tkey = data.keys()
	t2 = time.time()
	finalNode = {}
	print "CONNECTION TIME: "+str(t2 - t1)
	if not 'pages' in r2['query'].keys():
		print 'no pages'
		return {}
	if(Tkey[0] == "-1"):##Error Handling
		print "noLink "+name
		return finalNode
	
	fullNames = []
	shortWords = []
	
	info2 = data[Tkey[0]]['extract'].split("References")[0].replace('\\', " ")

	info2 = info2.lower()
	info2 = info2.encode('ascii',errors='ignore')
	if 'redirects' in r2['query']:
		links = getLinks(r2['query']['redirects'][0]['to'],data)
	else:
		links = getLinks(name,data)
	infoArray = info2.split()
	sortedLinks = []
	wordScore = 0
	finalNode['title'] = name
	finalNode['save'] = name.upper()
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
	print "LINK SORTING TIME: "+str(time6 - time5)
	print "TOTAL TIME: "+str(time6- t1)
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

def makeNode(initialNode):
	Tcount = 0
	newConnect = ""
	Ngraph = {}
	found = False
	time1 = 0
	time2 = 0
	time3 = 0
	time4 = 0
	time5 = 0
	wasHere = ""
	for query in initialNode['edges']:
		time1 = time.time()
		if not bool(collection.find_one({'save': query[0].upper()})):
			time3 = time.time()
			wasHere = ""
			newNode = generateNode(query[0])
			time4 = time.time()
			if(bool(newNode)):
				collection.insert_one(newNode)
				time5 = time.time()
		else:
			wasHere = " IS ALREADY HERE ^$^$^$^"
		time2 = time.time()
		print str(query)+"TIMES; LOOKUP : %f, NODE GENERATION: %f, INSERTION: %f, TOTAL: %f " % ((time3 - time1), (time4 - time3),(time5 - time4),(time2 - time1))
	#print json.dumps(Ngraph, indent=4, sort_keys=True)

def expand(counter):
	bounce = collection.find_one({'scanned': False})
	print "REDIRECT "+str(bounce['title'])+" ***********************************"
	del bounce['_id']
	makeGraph(bounce,counter)


def makeGraph(initialNode,counter,globalCount):
	searches = []
	Tgraph = {}
	TNode = {}
	dbNode = {}
	alreadyHere = False
	for item in initialNode['edges']:
		searches.append(item)
	while bool(searches):
		alreadyHere = False
		item = searches[0]
		if globalCount < 1:
			return Tgraph
		dbNode = collection.find_one({'save': item[0].upper()})
		if bool(dbNode):
			TNode = dbNode
			alreadyHere = True
			print TNode['save']+" "+str(TNode['scanned'])+" "+str(globalCount)+" IS ALREADY HERE!!!!"
			del TNode['_id']
		else:
			TNode = generateNode(item[0])
			print item[0]+" "+str(globalCount)+" New Connection *************"
		if(bool(TNode)):
			if not TNode['scanned']:
				TNode['scanned'] = True
				collection.update({'save':TNode['save']},{'$set':{'scanned':True} })
				makeNode(TNode)
				
				for edge in TNode['edges']:
					if not edge in searches:
						searches.append(edge)
				globalCount -= 1
		searches.remove(item)
		searches.sort(key=(lambda x: x[1]),reverse=True)
		print str(searches)+" SEARCH LIST ********"
	expand(globalCount)




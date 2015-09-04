import articleparser as ap
import Connect
import json
import sys
globalCount = 0

# if not len(sys.argv) > 1:
# 	collection = Connect.connect('wikiGraph','articleNodesTest')
# 	ap.collection = collection
# else:
# 	collection = Connect.connect('wikiGraph','articleNodesTest',sys.argv[1],int(sys.argv[2]))
# 	ap.collection = collection
	
collection = Connect.connect('wikiGraph','articleNodesTest','104.131.67.157',40000)
#generateNode takes in the name(string) of the node and outputs a node object
#main
library = open("library.json","w+")
while (True):
	search = raw_input("what do you want to search (type 'resave' to refresh the database)? ")
	if ("addnode" in search):
		searchParam = search.split()
		globalCount = int(searchParam[2])
		ap.makeGraph(ap.generateNode(searchParam[1].replace("_"," ")),int(searchParam[2]))
	elif ("test" in search):
		searchParam = search.split()
		ap.makeNode(ap.generateNode(searchParam[1].replace("_"," ")))
	elif ("expand" in search):
		searchParam = search.split()
		globalCount = int(searchParam[1])
		ap.expand(globalCount)
	elif('path' in search):
		searchParam = search.split()
		print ap.find_path(searchParam[1],searchParam[2])
	elif(search != ""):
		node = ap.generateNode(search)
		print json.dumps(node, indent=4, sort_keys=True)
		if not bool(collection.find_one({'save': node['save']})):
			collection.insert_one(node)
		else:
			print "ALREADY HERE!!!"
	else:
		break

#takes in an initial node and makes a counter number of new nodes

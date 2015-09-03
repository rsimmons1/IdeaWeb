import articleparser as ap
import Connect
import json
globalCount = 0
collection = Connect.connect('wikiGraph','articleNodesTest')

#generateNode takes in the name(string) of the node and outputs a node object


#main
library = open("library.json","w+")
while (True):
	search = raw_input("what do you want to search (type 'resave' to refresh the database)? ")
	if ("addnode" in search):
		searchParam = search.split()
		globalCount = int(searchParam[2])
		ap.makeGraph(ap.generateNode(searchParam[1].replace("_"," ")),int(searchParam[2]),globalCount)
	elif ("test" in search):
		searchParam = search.split()
		ap.makeNode(ap.generateNode(searchParam[1].replace("_"," ")))
	# elif ("expand" in search):
	# 	searchParam = search.split()
	# 	globalCount = int(searchParam[1])
	# 	for x in range(int(searchParam[2])):
	# 		thread.start_new_thread(expand,tuple([int(searchParam[1])]))
	# 		time.sleep(1)
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

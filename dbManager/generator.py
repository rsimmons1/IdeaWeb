import articleparser as ap
import Connect
import json
import sys
from Queue import *
globalCount = 0

# if not len(sys.argv) > 1:
# 	collection = Connect.connect('wikiGraph','articleNodesTest')
# 	ap.collection = collection
# else:
# 	collection = Connect.connect('wikiGraph','articleNodesTest',sys.argv[1],int(sys.argv[2]))
# 	ap.collection = collection
	
collection = Connect.connect('wikiGraph','articleNodesTest','104.131.67.157',40000)
# collection = Connect.connect('wikiGraph','articleNodesTest')

def findPath(start,goal,graph,depth=5):
	assert (graph.find_one({'save':start.upper()}) and bool(graph.find_one({'save':goal.upper()})))
	frontier = Queue()
	frontier.put(start)
	came_from = {}
	came_from[start] = None
	found = False
	while not frontier.empty() and not found:
	   current = frontier.get()
	   exists = graph.find_one({'save':current.upper()})
	   if bool(exists):
		   edges = map(lambda x: x[0],graph.find_one({'save':current.upper()})['edges'])[:depth]
		   for next in edges:
		      if next not in came_from:
		         frontier.put(next)
		         came_from[next] = current
		         if next.lower() == goal.lower():
		         	found = True
		         	goal = next
		      		break
	current = goal
	path = [current]

	while current != start:
	   current = came_from[current]
	   path.append(current)
	path.reverse()
	return path
	

#generateNode takes in the name(string) of the node and outputs a node object
#main
path1 = findPath('physics','radiation',collection)
print path1

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
		print findPath(searchParam[1].replace("_"," "),searchParam[2].replace("_"," "),collection)
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

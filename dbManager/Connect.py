#!/usr/bin/python
from pymongo import MongoClient
from collections import deque
def connect(dbName,colName,website=None,port=None):
	client = MongoClient(website,port)
	db = client[dbName]
	return db[colName]

def find_path(collection,start, end, path=[],searches=[]):
	Node = {}
	if searches:
		del searches[0]
	print start
	path = path + [start.lower()]
	Node = collection.find_one({'save':start.upper()})
	newpath = []
	if start.lower() == end.lower():
		return path
	if bool(Node):
		searches += Node['edges'][:5]
	for edge in searches:
		if not edge[0].lower() in path and not edge[0].lower() in searches:
			newpath = find_path(collection,searches[0][0], end, path)
		if newpath: 
			return newpath
	return None

def breadth_first_search(graph, start, goal,depth=5):
    frontier = deque()
    frontier.append(start)
    came_from = {}
    came_from[start] = None
    path = []
    found = False
    while not (len(frontier) == 0) and not found:
        current = frontier.popleft()
        path.append(current)
        if current.lower() == goal.lower():
            break
        edges = graph.find_one({'save':current.upper()})
        if bool(edges):
	        for next in edges['edges'][:depth]:
	            if next[0] not in came_from:
	                frontier.append(next[0])
	                came_from[next[0]] = current
	            if next[0].lower() == goal.lower():
	            	path.append(goal)
	            	found = True
	            	break
    
    return came_from





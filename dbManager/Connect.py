#!/usr/bin/python
from pymongo import MongoClient
from collections import deque
def connect(dbName,colName,website=None,port=None):
	client = MongoClient(website,port)
	db = client[dbName]
	return db[colName]

def neighbors(node,depth=5):
	return map(lambda x: x[0],node['edges'][:depth])

def find(word,graph):
	return graph.find_one({'save':word.upper()})

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
            return came_from
        edges = neighbors(find(current))
        if bool(edges):
	        for next in edges:
	            if next not in came_from:
	                frontier.append(next)
	                came_from[next] = current
	            if next.lower() == goal.lower():
	            	came_from[next] = current
	            	path.append(goal)
	            	found = True
	            	return came_from
    return None
    

def exact_path(graph,start,end,path=[]):
	if start.lower() == end.lower():
		return path
	for item in graph:
		if item.lower() == end.lower():
			path.append(item)
			return exact_path(graph,start,graph[item])





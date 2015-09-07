from django.shortcuts import render
import json
from dbManager import articleparser as parse
from dbManager import Connect

#from django_ajax.decorators import ajax
# Create your views here.
collection = Connect.connect('wikiGraph','articleNodesTest','104.131.67.157',40000)
parse.collection = collection

from django.http import HttpResponse

def index(request):
    return render(request,'ideaWeb/index.html',{})

#@ajax
def ajax_request(request):
	info = {}
	query = request.GET.get('q','')
	info = collection.find_one({'save':query.upper()})
	if bool(info):
		del info['_id']

	else:
		print "NewNode"
		info = parse.generateNode(query)
		if bool(info):
			collection.insert_one(info)
			del info['_id']
	return HttpResponse(json.dumps(info))


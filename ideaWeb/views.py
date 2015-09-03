from django.shortcuts import render
import json
import Connect
from dbManager import articleparser as parse
#from django_ajax.decorators import ajax
# Create your views here.

from django.http import HttpResponse

def index(request):
    return render(request,'ideaWeb/index.html',{})

#@ajax
def ajax_request(request):
	query = request.GET.get('q','')
	collections = Connect.connect('wikiGraph','articleNodesTest')
	info = collections.find_one({'save':query.upper()})
	if info:
		del info['_id']
	else:
		info = parse.generateNode(query)
		collections.insert_one(info)
	return HttpResponse(json.dumps(info))


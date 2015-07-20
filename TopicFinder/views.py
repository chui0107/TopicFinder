from django.shortcuts import render
import requests

def Search(topic): 
	result = {'wiki':['haha', 'cong'], 'twitter':['1']}
	return result;

def ShowMain(request):
	response = {"status" : 1, "message" : None , "topics" : None}
	return render(request, 'host.html', {'response': response})

def SearchTopic(request):

	response = {"status" : 0, "message" : None , "topics" : None}
	if request.method == 'GET':
		
		topic = request.GET["topic"]
		if topic == None or topic == "" :
			response["message"] = "Topic can't be none"
			return render(request, 'host.html', {'response': response})
		
		response["status"] = 1
		response["topics"] = Search(topic)
		
		return render(request, 'host.html', {'response': response})
	
	response["message"] = "This page can only accept GET request for now"
	return render(request, 'host.html', {'response': response})
	

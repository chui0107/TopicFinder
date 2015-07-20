from django.shortcuts import render
import requests

def Search(topic, result):
	
	status = True
	wiki = "https://en.wikipedia.org/w/api.php"
	params = {'action' : 'opensearch', 'search':topic}
	r = requests.get(wiki, params=params)
	
	if r.status_code == 200:
		response = r.json()
		result['wiki'] = zip(response[1], response[3])
	else:
		status = False
		
	twitter = "https://en.wikipedia.org/w/api.php"
	# params = {'action' : 'opensearch', 'search':topic}
	# r = requests.get(wiki + responseFormat, params=params)
	
	'''
	if r.status_code == 200:
		response = r.json()
		result['wiki'] = response
	'''
	
	return status

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
		
		result = {'wiki':[], 'twitter':[]}
		status = Search(topic, result)
		if status:
			response["status"] = 1
			response["topics"] = result
		
		print response
		return render(request, 'host.html', {'response': response})
	
	response["message"] = "This page can only accept GET request for now"
	return render(request, 'host.html', {'response': response})
	

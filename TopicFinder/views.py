from django.shortcuts import render
import requests
import URLregex
import re

def Search(topic, result):
	status = 1
	result = result["topics"]	
	wiki = "https://en.wikipedia.org/w/api.php"
	params = {'action' : 'opensearch', 'search':topic}
	r = requests.get(wiki, params=params)
	
	if r.status_code == 200:
		response = r.json()
		result['wiki'] = zip(response[1], response[3])
	else:
		status = 0
	
	headers = {'Authorization': 'Basic VkxXMGZod3FBYmliVVNTYmNlNTd4Q1JTSjowajJtWVZ4eGRXZ3hHaDczWm9INEVuMnNCTVB0SDNkRzQ5bDk5YzdHQktQd0Q4Vm1TVw==', 'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'}	
	twitter = 'https://api.twitter.com/oauth2/token'	
	data = {'grant_type':'client_credentials'}
	
	r = requests.post(twitter, headers=headers, data=data, params=params)
	
	if r.status_code == 200:
		response = r.json()
		if response['token_type'] == 'bearer':
			token = response['access_token'] 
			twitter = 'https://api.twitter.com/1.1/search/tweets.json'
			params = {'q': topic, 'lang':'en'}
			headers = {'Authorization':'Bearer ' + token}
			r = requests.get(twitter, params=params, headers=headers)
			
			if r.status_code == 200:
				response = r.json()
				tweets = []
				urls = []
				
				for each in response['statuses']:
					text = each['text']
					match = re.findall(URLregex.URL_REGEX, text)
					if len(match):
						urls.append(match[0])
					tweets.append(re.sub(URLregex.URL_REGEX, '', text))
					
				result['twitter'] = zip(tweets, urls)
				return status
	
	status = 0
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
		
		response["topics"] = {'wiki':None, 'twitter':None} 
		status = Search(topic, response)
		if status == 0:
			response['message'] = 'An error has occurred'
		response["status"] = 1	
		return render(request, 'host.html', {'response': response})
	
	response["message"] = "This page can only accept GET request for now"
	return render(request, 'host.html', {'response': response})
	

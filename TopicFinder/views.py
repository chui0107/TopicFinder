from django.shortcuts import render
import requests
import URLregex
import re

TestMode = False

def Search(topic, apis, result):
	status = True
	result = result["topics"]	
	wiki = apis[0]
	params = {'action' : 'opensearch', 'search':topic}
	r = requests.get(wiki, params=params)
	
	if r.status_code == 200:
		response = r.json()
		result['wiki'] = zip(response[1], response[3])
	else:
		status = False
	
	headers = {'Authorization': 'Basic VkxXMGZod3FBYmliVVNTYmNlNTd4Q1JTSjowajJtWVZ4eGRXZ3hHaDczWm9INEVuMnNCTVB0SDNkRzQ5bDk5YzdHQktQd0Q4Vm1TVw==', 'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'}	
	twitter = apis[1]	
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
	
	status = False
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
		
		global TestMode
		if TestMode == False:
			apis = ['https://en.wikipedia.org/w/api.php', 'https://api.twitter.com/oauth2/token']
			status = Search(topic, apis, response)
			if status == False:
				response['message'] = 'An error has occurred'
			response["status"] = 1
			return render(request, 'host.html', {'response': response})
	
		else:
			testResult = True
			# test set 1
			apis = ['https://en.wikipedia.org/w/api1.php', 'https://api.twitter.com/oauth2/token1']
			testResult &= (Search(topic, apis, response) == False)
			if testResult == False:
				print 'TestSet1 failed'
			# test set 2
			apis = ['https://en.wikipedia.org/w/api.php', 'https://api.twitter.com/oauth2/token1']
			testResult &= (Search(topic, apis, response) == False)
			if testResult == False:
				print 'TestSet2 failed'
			
			# test set 3
			apis = ['https://en.wikipedia.org/w/api1.php', 'https://api.twitter.com/oauth2/token']
			testResult &= (Search(topic, apis, response) == False)
			if testResult == False:
				print 'TestSet3 failed'
			
			# test set 4
			apis = ['https://en.wikipedia.org/w/api.php', 'https://api.twitter.com/oauth2/token']
			testResult &= (Search(topic, apis, response) == True)
			if testResult == False:
				print 'TestSet4 failed'
				
			if testResult:
				print 'Passed all tests'
				
			response["message"] = 'testing mode'
			return render(request, 'host.html', {'response': response})
		
	response["message"] = "This page can only accept GET request for now"
	return render(request, 'host.html', {'response': response})
	
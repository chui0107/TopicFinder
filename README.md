To run the program:
   1. Make sure you have python Django installed.
   2. Navigate to TopicFinder folder, run "python manage.py runserver" on the commond line in that folder
   3. Now the server should be running at http://localhost:8000/
   4. Type in the topic in the input box you want to search for
   5. The results from both Wiki and Twitter should show up below the input box

Note: the program could also be run with Pydev plungin fo eclipse. Just open the eclipse project and run the project from the root level.

To run the unit test:
	There is a global variable in the views.py called TestMode, toggle that to be true to run the 
	unitest on the Search function, it covers 4 different cases where both APIs could have different
	results. You should see a printout from the console that says 'Passed all tests' after this
	
Performance Profile:
    The biggest bottleneck comes from Search function where querying both APIs are in sequence and it
	is a blocking call. When the number of queries scale, i.e. need to crawl from lots of different
	sources, it could be turned into a multithreaded architecture and with the async calls
	to each source and managed by a event queue.
	
	
NOTES: html action to trigger the server script by its name
<form id = "searchForm" method="GET" action="{% url 'search' %}">
	=> url(r'^/search$', 'TopicFinder.views.SearchTopic', name='search'),
	
urls.py match addresses to handers by names
url(r'^$', 'TopicFinder.views.ShowMain', name='home') => def ShowMain(request):

mind the same origin policy, JS are supposed to only talk to its own domain.
The unit test in this project is far from perfect, it should be replaced with more structured testing scheme

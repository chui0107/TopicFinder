from django.shortcuts import render

def ShowMain(request):
	return render(request, 'host.html', None)
	
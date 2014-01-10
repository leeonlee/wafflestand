from django.shortcuts import render
from django.http import HttpResponse
import json
from bluray.models import *
# Create your views here.

def index(request):
	movie_list = Movie.objects.all()
	context = {
		'movie_list' : movie_list
	}

	return render(request, 'bluray/index.html', context)

def track(request):
	results = {'success':False}
	if request.method == 'GET':
		GET = request.GET
		if GET.has_key('pk') and GET.has_key('vote'):
			pk = int(GET['pk'])
			vote = GET['vote']

			movie = Movie.objects.get(id=pk)
			print movie.name
			if vote == 'up':
				movie.name = 'jerk'
			elif vote == 'down':
				movie.name = 'off'
			movie.save()
			results = {'success':True}

	jason = json.dumps(results)
	print 'hi'
	return HttpResponse(jason, content_type='application/json')

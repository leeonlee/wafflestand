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
		if GET.has_key('id') and GET.has_key('track'):
			id_in = int(GET['id'])
			track  = GET['track']

			movie = Movie.objects.get(id=id_in)
			'''
			if track = 'track' then add user to movie's track list
			if track == 'untrack' then remove
			find user through User.objects.get(username = request.user)
			should probably make sure user is logged in
			'''
			movie.save()
			results = {'success':True}

	jason = json.dumps(results)
	return HttpResponse(jason, content_type='application/json')

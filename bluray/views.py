from django.shortcuts import render
from django.http import HttpResponse
import json
from bluray.models import *
# Create your views here.

def index(request):
	movie_list = Movie.objects.filter(released=False)
	context = {
		'movie_list' : movie_list
	}

	return render(request, 'bluray/index.html', context)

'''
should probably make sure user is logged in
'''
def track(request):
	results = {'success':False}
	if request.method == 'GET':
		GET = request.GET
		if GET.has_key('id') and GET.has_key('track'):
			id_in = int(GET['id'])
			track = GET['track']
			user = request.user

			movie = Movie.objects.get(id=id_in)
			if track == "track":
				movie.tracking.add(user)
			elif track == "untrack":
				movie.tracking.remove(user)
			movie.save()
			results = {'success':True}

	jason = json.dumps(results)
	return HttpResponse(jason, content_type='application/json')

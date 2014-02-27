from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from bluray.models import *
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
	movie_list = Movie.objects.filter(released=False)
	login_form = LoginForm()
	reset_form = ResetForm()
	try:
		context = {
			'user_tracking' : [movie.name for movie in request.user.movie_set.all()],
			'movie_list' : movie_list,
			'login_form' : login_form,
			'reset_form' : reset_form,
		}
	except:
		context = {
			'user_tracking' : [],
			'movie_list' : movie_list,
			'login_form' : login_form,
			'reset_form': reset_form,
		}

	return render(request, 'bluray/index.html', context)

# track button no longer shows up unless user is logged in
def track(request):
	results = {'success':'False'}
	if request.method == 'GET' and request.is_ajax():
		GET = request.GET
		if GET.has_key('id') and GET.has_key('track'):
			id_in = int(GET['id'])
			track = GET['track']
			user = request.user

			movie = Movie.objects.get(rt_id=id_in)
			if track == "Track":
				movie.tracking.add(user)
			elif track == "Untrack":
				movie.tracking.remove(user)
			movie.save()
			success = '%s %s' %(user.username, track)
			results = {'success':success}

	jason = json.dumps(results)
	return HttpResponse(jason, content_type='application/json')

def loginview(request):
	results = {'success':'invalid'}
	if request.method == 'POST' and request.is_ajax():
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					results['success'] = 'success'
				else:
					results['success'] = 'validate'

	response = json.dumps(results)
	return HttpResponse(response, content_type='application/json')

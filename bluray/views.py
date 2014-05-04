from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from bluray.models import *
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request, query = 'index'):
	movie_list = Movie.objects.all()
	active = query
	# sort parameter
	sort = request.GET.get('sort_by', None)
	
	if query == 'comingSoon':
		movie_list = Movie.objects.filter(released=False).exclude(release=None).order_by('release')
	elif query == 'freshOut':
		movie_list = Movie.objects.filter(released=True).order_by('-release')
	elif query == 'myMovies':
		movie_list = request.user.movie_set.all()
	elif query == 'index':
		if sort:
			movie_list = Movie.objects.filter(released=False).order_by(sort)
		else:
			movie_list = Movie.objects.filter(released=False)			
	else:
		raise Http404

	login_form = LoginForm()
	reset_form = ResetForm()

	context = {
		'movie_list' : movie_list,
		'login_form' : login_form,
		'reset_form' : reset_form,
		'active' : active,
	}

	if request.user.is_authenticated():
		context['user_tracking'] = [movie.name for movie in request.user.movie_set.all()]

	return render(request, 'bluray/index.html', context)

# track button no longer shows up unless user is logged in
def follow(request):
	results = {'success':'False'}
	if request.method == 'GET' and request.is_ajax():
		GET = request.GET
		if GET.has_key('id') and GET.has_key('follow'):
			id_in = int(GET['id'])
			follow = GET['follow']
			user = request.user

			movie = Movie.objects.get(rt_id=id_in)
			if follow == "Follow":
				movie.following.add(user)
			elif follow == "Unfollow":
				movie.following.remove(user)
			movie.save()
			success = '%s %s' %(user.username, follow)
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

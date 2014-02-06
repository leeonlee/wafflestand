from django.conf.urls import patterns, url

from bluray import views

urlpatterns = patterns('',
    url(r'^track/$', views.track, name='track'),
    url(r'^loginview/$', views.loginview, name='login'),
    url(r'logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^$', views.index, name='index'),
)

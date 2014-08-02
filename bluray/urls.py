from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views

from bluray import views

from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView


urlpatterns = patterns('',
    url(r'^follow/$', views.follow, name='follow'),
    url(r'^loginview/$', views.loginview, name='login'),
    url(r'logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^sortmovies/$', views.sortMovies, name='sortmovies'),
    
    url(r'^accounts/password/change/$', auth_views.password_change, name='password_change'),
    url(r'^accounts/password/change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^accounts/password/reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^accounts/password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^accounts/password/reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^$', views.index, name='index'),
    url(r'(?P<query>\w+)/$', views.index, name='index'),
)

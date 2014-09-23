from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include('bluray.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

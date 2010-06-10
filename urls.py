from django.conf.urls.defaults import *
from django.conf import settings

from registration.views import register
from uniformzulu.forms import ReCaptchaRegistrationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r"^%s(?P<path>.*)" % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,'show_indexes': True}),

	(r'^accounts/login/', 'django.contrib.auth.views.login', {'redirect_field_name': 'next'}),
	(r'^accounts/logout/', 'django.contrib.auth.views.logout'),
	
	# django-registration
	url(r'^accounts/register/$', register, {'form_class': ReCaptchaRegistrationForm, 'backend': 'registration.backends.default.DefaultBackend'}, name='registration_register'),
	(r'^accounts/', include('registration.backends.default.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    
	(r'^', include('UniformZulu.uniformzulu.urls')),
)

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
	(r'^$', 'uniformzulu.views.main'),
	(r'^get_quiz/(\d+)/$', 'uniformzulu.views.get_quiz'),
	(r'^get_quiz_hard/(\d+)/$', 'uniformzulu.views.get_quiz_hard'),
#	(r'quiz/(?P<uuid>.*)$', 'uniformzulu.views.quiz_form'),
	url(r'quiz/(?P<uuid>.*)$', 'uniformzulu.views.quiz_form', name="quiz_form"),
#	(r'^xd_receiver\.htm$', 'uniformzulu.views.xd_receiver'),

#	(r'^facebook/', include('facebookconnect.urls')),

    (r'^comments/', include('django.contrib.comments.urls')),

)

if settings.DEVELOPMENT:
	urlpatterns += patterns('',
		(r'^facebook/', include('facebookconnect.urls')),
	)
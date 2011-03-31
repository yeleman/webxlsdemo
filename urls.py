#!/usr/bin/env python

from django.conf.urls.defaults import *
from settings import STATIC_ROOT
from django.contrib import admin
admin.autodiscover()

import web.views as views

urlpatterns = patterns('',
     url(r'^/?$', views.index, name='index'),
     url(r'^add/?$', views.add, name='add'),
     url(r'^view/([0-9]+)/?$', views.view, name='view'),
     url(r'^login/$', 'django.contrib.auth.views.login', \
         {'template_name': 'login_django.html'}, name='login'),
     url(r'^logout/$', 'django.contrib.auth.views.logout', \
         {'template_name': 'logout_django.html'}, name='logout'),


    url(r'^static/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': STATIC_ROOT, 'show_indexes': True}, \
             name='static'),

    (r'^admin/', include(admin.site.urls)),
)

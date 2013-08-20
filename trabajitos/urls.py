# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.user import views
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'trabajitos.views.home', name='home'),
    # url(r'^trabajitos/', include('trabajitos.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginu, name='login'),
    url(r'^logout/$', views.logoutu, name='home'),
    
    url(r'^home/$', views.home, name='home'),
    
    url(r'^addfind/$', views.addfind, name='addfind'),
    url(r'^addalert/$', views.addalert, name='addalert'),
    url(r'^mysearchs/', views.mysearchs, name='mysearchs'),
    url(r'^myfinds/(?P<count>\d{1,40})/$', views.myfinds, name='myfinds'),
    url(r'^deletefind/(?P<id>\d{1,40})/$', views.deletefind, name='deletefind'),
    url(r'^deletealert/(?P<id>\d{1,40})/$', views.deletealert, name='deletealert'),
    url(r'^mygoodfinds/(?P<count>\d{1,40})/$', views.mygoodfinds, name='mygoodfinds'),
    url(r'^myjobalert/(?P<count>\d{1,40})/$', views.myjobalert, name='myjobalert'),
    url(r'^myalerts/', views.myalerts, name='myalerts'),
    url(r'^changeaccount/', views.changeaccount, name='changeaccount'),
    url(r'^myjobs/(?P<id>\d{1,40})/$', views.myjobs, name='myjobs'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    
    url(r'^admin/', include(admin.site.urls)),
)

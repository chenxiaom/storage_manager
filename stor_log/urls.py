# coding:utf-8
from django.conf.urls import patterns, include, url
from stor_log.views import *

urlpatterns = patterns('',
    url(r'^$', time_line),
)
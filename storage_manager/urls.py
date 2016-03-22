# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    (r'^$', 'storage_manager.views.index'),
    (r'^profile/$', 'storage_manager.views.profile'),
    (r'^lsuser/$', 'storage_manager.views.lsuser'),
    (r'^user_add/$', 'storage_manager.views.user_add'),
    (r'^user_list/$', 'storage_manager.views.user_list'),
    (r'^login/$', 'storage_manager.views.login'),
    (r'^logout/$', 'storage_manager.views.logout'),
    (r'^time_line/$',include('stor_log.urls')),
    (r'^stor_idc/', include('stor_idc.urls')),
    (r'^stor_info/', include('stor_info.urls')),

)

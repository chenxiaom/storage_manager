# coding:utf-8
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response
from storage_manager.api import *
from django.http import HttpResponseNotFound

def time_line(request):
    header_title, path1, path2 = '事件时间轴', '平台事件记录', '时间轴'
    logs = Logs.objects.order_by("-start_time")
    return render_to_response('timeline_v2.html', locals(), context_instance=RequestContext(request))

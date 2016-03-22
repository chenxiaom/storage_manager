# coding: utf-8
import os
import json
import ldap
import getpass
import hashlib
import datetime
import subprocess
import crypt
from ldap import modlist
from Crypto.Cipher import AES
from stor_idc.models import IDCS, Builds, Floors
from stor_info.models import StorageInfos, StorHosts, StorModels
from storage_manager.models import Users, UserGroups, DEPTS
from stor_log.models import *
from stor_log.views import *
from ConfigParser import ConfigParser
from binascii import b2a_hex, a2b_hex
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, InvalidPage

#密码加密方法
def md5_crypt(string):
    return hashlib.new("md5", string).hexdigest()

def require_login(func):
    """要求登录的装饰器"""
    def _deco(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return HttpResponseRedirect('/login/')
        return func(request, *args, **kwargs)
    return _deco

#判断是否属于普通用户
def is_common_user(request):
    if request.session.get('role_id') == 0:
        return True
    else:
        return False

#判断是否属于超级用户
def is_super_user(request):
    if request.session.get('role_id') == 2:
        return True
    else:
        return False

#判断是否属于管理组
def is_group_admin(request):
    if request.session.get('role_id') == 1:
        return True
    else:
        return False

#判断是否属于普通用户
def is_common_user(request):
    if request.session.get('role_id') == 0:
        return True
    else:
        return False

def get_user_dept(request):
    user_id = request.session.get('user_id')
    if user_id:
        user_dept = Users.objects.get(id=user_id).dept
        return user_dept.id


def page_list_return(total, current=1):
    min_page = current - 2 if current - 4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total

    return range(min_page, max_page+1)

def pages(posts, r):
    """分页公用函数"""
    contact_list = posts
    p = paginator = Paginator(contact_list, 10)
    try:
        current_page = int(r.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(p.page_range), current_page)

    try:
        contacts = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        contacts = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0
    if current_page <= (len(p.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

    return contact_list, p, contacts, page_range, current_page, show_first, show_end

@require_login
def get_session_user_info(request):
    user_id = request.session.get('user_id', 0)
    user = Users.objects.filter(id=user_id)
    if user:
        user = user[0]
        dept = user.dept
        return [user.id, user.username, user, dept.id, dept.name, dept]

def get_session_user_dept(request):
    user_id = request.session.get('user_id', 0)
    user = Users.objects.filter(id=user_id)
    if user:
        user = user[0]
        dept = user.dept
        return user, dept

#添加日志记录
#db_add_record(user=user,event_type='Add',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now())
def db_change_record(**kwargs):
    #name = kwargs.get('name')
    #group = Floors.objects.filter(name=name)
    #users = kwargs.pop('users')
    #if group:
    #    raise AddError(u'楼层 %s 已经存在' % name)
    add_record = Logs(**kwargs)
    add_record.save()

def httperror(request, emg):
    message = emg
    return render_to_response('error.html', locals())
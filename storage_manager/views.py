# -*- coding: utf-8 -*-

import uuid
import urllib
import paramiko
from django.db.models import Q
#from __future__ import division
from storage_manager.api import *
from django.db.models import Count
from django.template import RequestContext
from django.db.models import Sum
from django.shortcuts import render_to_response,render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound,HttpResponseRedirect,HttpResponse


def lsuser(request):
    html='this is lsuser mth.'
    #html = User.objects.all()
    return HttpResponse(html)

def jstree(request):
    #html='this is lsuser mth.'
    #html = User.objects.all()
    return render(request,'tree_view.html')
    #return render_to_response('tree_view.html')




def getDaysByNum(num):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    li_date, li_str = [], []
    for i in range(0, num):
        today = today-oneday
        li_date.append(today)
        li_str.append(str(today)[5:10])
    li_date.reverse()
    li_str.reverse()
    t = (li_date, li_str)
    return t


def login(request):
    """登录界面"""
    if request.session.get('username'):
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render_to_response('login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_filter = Users.objects.filter(username=username)
        if user_filter:
            user = user_filter[0]
            if md5_crypt(password) == user.password:
                request.session['user_id'] = user.id
                user_filter.update(last_login=datetime.datetime.now())
                if user.role == 'SU':
                    request.session['role_id'] = 2
                elif user.role == 'DA':
                    request.session['role_id'] = 1
                else:
                    request.session['role_id'] = 0
                response = HttpResponseRedirect('/', )
                response.set_cookie('username', username, expires=604800)
                response.set_cookie('seed', md5_crypt(password), expires=604800)
                user = request.session.get('user_id')
                msg_title=u'用户登录'
                msg = u' %s 用户登录成功！' % username
                db_change_record(user=user,event_type='LS',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now())
                return response
            else:
                error = '密码错误，请重新输入。'
        else:
            error = '用户不存在。'
    return render_to_response('login.html', {'error': error})

def logout(request):
    request.session.delete()
    return HttpResponseRedirect('/login/')

@require_login
def index_cu(request):
    user_id = request.session.get('user_id')
    user = Users.objects.filter(id=user_id)
    if user:
        user = user[0]
    login_types = {'L': 'LDAP', 'M': 'MAP'}
    user_id = request.session.get('user_id')
    username = Users.objects.get(id=user_id).username
    new_posts = []
    post_five = []

    return render_to_response('index_cu.html', locals(), context_instance=RequestContext(request))


@require_login
def index(request):
    li_date, li_str = getDaysByNum(7)
    today = datetime.datetime.now().day
    from_week = datetime.datetime.now() - datetime.timedelta(days=7)

    if is_super_user(request):
        users = Users.objects.all()
        storages = StorageInfos.objects.all()
        hosts = StorHosts.objects.all()
        #all_ldevs_count = StorageInfos.objects.count(stor_ldevs_count)
        all_ldevs_count = StorageInfos.objects.aggregate(Sum('stor_ldevs_count'))   #所有存储的LDEV个数
        all_bare_count = StorageInfos.objects.aggregate(Sum('stor_bare_capacity'))    #所有存储的裸容量
        all_space_count = StorageInfos.objects.aggregate(Sum('stor_space_capacity'))   #所有存储RAID后的容量

        all_remain_ldevs_count = StorageInfos.objects.aggregate(Sum('stor_remain_ldevs'))   #剩余Ldev个数
        all_remain_space_count = StorageInfos.objects.aggregate(Sum('stor_remain_capacity'))    #剩余容量

        all_allocated_ldev_count = StorHosts.objects.aggregate(Sum('host_ldev_count')) ; #所有主机已使用的Ldev个数
        all_allocated_space_count = StorHosts.objects.aggregate(Sum('host_allocated_size')) ; #所有主机已使用的容量

        #all_ldevs_count=123
        #online = Log.objects.filter(is_finished=0)
        #online_host = online.values('host').distinct()
        #online_user = online.values('user').distinct()
        active_users = Users.objects.filter(is_active=1)
        active_storages = StorageInfos.objects.filter(is_active=1)
        #week_data = Log.objects.filter(start_time__range=[from_week, datetime.datetime.now()])
    if is_common_user(request):
        users = Users.objects.all()
        storages = StorageInfos.objects.all()
        active_users = Users.objects.filter(is_active=1)
        active_storages = StorageInfos.objects.filter(is_active=1)

    elif is_group_admin(request):
        user = get_session_user_info(request)[2]
        dept_name, dept = get_session_user_info(request)[4:]
        users = Users.objects.filter(dept=dept)
        storages = StorageInfos.objects.filter(stor_is_active=1)
        #online = Log.objects.filter(dept_name=dept_name, is_finished=0)
        #online_host = online.values('host').distinct()
        #online_user = online.values('user').distinct()
        active_users = users.filter(is_active=1)
        active_storages = storages.filter(stor_is_active=1)
        #week_data = Log.objects.filter(dept_name=dept_name, start_time__range=[from_week, datetime.datetime.now()])

    # percent of dashboard
    if users.count() == 0:
        percent_user, percent_online_user = '0%', '0%'
    else:
        percent_user = format(active_users.count() / users.count(), '.0%')
        #percent_online_user = format(online_user.count() / users.count(), '.0%')
    if storages.count() == 0:
        percent_host, percent_online_host = '0%', '0%'
    else:
        percent_host = format(active_storages.count() / storages.count(), '.0%')
        #percent_online_host = format(online_host.count() / hosts.count(), '.0%')
    if all_ldevs_count == 0 :
        ldevs_count ='0%', '0%'
    else:
        ldevs_count = format(2 / 3, '.0%')

    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
    #return render_to_response('index.html')


def profile(request):
    #user_id = request.session.get('user_id')
    user_id = request.GET.get('user_id')
    if not user_id:
        return HttpResponseRedirect('/')
    user = Users.objects.get(id=user_id)
    return render_to_response('profile.html', locals(), context_instance=RequestContext(request))



def skin_config(request):
    return render_to_response('skin_config.html')


class AddError(Exception):
    pass

def db_add_user(**kwargs):
    groups_post = kwargs.pop('groups')
    user = Users(**kwargs)
    user.save()
    if groups_post:
        group_select = []
        for group_id in groups_post:
            group = UserGroups.objects.filter(id=group_id)
            group_select.extend(group)
        user.group = group_select
    return user

def db_del_user(username):
    try:
        user = Users.objects.get(username=username)
        user.delete()
    except ObjectDoesNotExist:
        pass

def user_add(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '添加用户', '用户管理', '添加用户'
    user_role = {'SU': u'超级管理员', 'DA': u'部门管理员', 'CU': u'普通用户'}
    dept_all = DEPTS.objects.all()
    group_all = UserGroups.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username', '')
        #password = gen_rand_pwd(16)
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        dept_id = request.POST.get('dept_id')
        groups = request.POST.getlist('groups', [])
        role_post = request.POST.get('role', 'SU')
        is_active = True if request.POST.get('is_active', '1') == '1' else False

        try:
            if '' in [username, password, name, groups, role_post, is_active]:
                error = u'带*内容不能为空'
                raise AddError
            user = Users.objects.filter(username=username)
            if user:
                error = u'用户 %s 已存在' % username
                raise AddError

            dept = DEPTS.objects.filter(id=dept_id)
            if dept:
                dept = dept[0]
            else:
                error = u'部门不存在'
                raise AddError(error)

        except AddError:
            pass
        else:
            try:
                user = db_add_user(username=username,
                                   password=md5_crypt(password),
                                   name=name, email=email, dept=dept,
                                   groups=groups, role=role_post,
                                   is_active=is_active,
                                   date_joined=datetime.datetime.now())
                mail_title = u'恭喜用户添加成功'
            except Exception, e:
                error = u'添加用户 %s 失败 %s ' % (username, e)
                try:
                    db_del_user(username)
                except Exception:
                    pass
            else:
                user = request.session.get('user_id')
                msg_title=u'新增用户'
                msg = u'添加用户 %s 成功！' % username
                db_change_record(user=user,event_type='AU',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now())

    return render_to_response('user_add.html', locals(), context_instance=RequestContext(request))


def user_list(request):
    user_role = {'SU': u'超级管理员', 'GA': u'组管理员', 'CU': u'普通用户'}
    header_title, path1, path2 = '查看用户', '用户管理', '用户列表'
    keyword = request.GET.get('keyword', '')
    gid = request.GET.get('gid', '')
    did = request.GET.get('did', '')
    contact_list = Users.objects.all().order_by('name')
    #db_del_user('chenxm')

    if gid:
        user_group = UserGroups.objects.filter(id=gid)
        if user_group:
            user_group = user_group[0]
            contact_list = user_group.user_set.all()

    if did:
        dept = DEPTS.objects.filter(id=did)
        if dept:
            dept = dept[0]
            contact_list = dept.user_set.all().order_by('name')

    if keyword:
        contact_list = contact_list.filter(Q(username__icontains=keyword) | Q(name__icontains=keyword)).order_by('name')

    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(contact_list, request)

    return render_to_response('user_list.html', locals(), context_instance=RequestContext(request))

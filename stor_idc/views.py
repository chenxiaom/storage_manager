# coding:utf-8
from django.shortcuts import render
import datetime
from django.db.models import Q
from storage_manager.api import *
from django.template import RequestContext
from django.shortcuts import get_object_or_404

# Create your views here.
def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))

def idc_add(request):
    """ 添加IDC """
    header_title, path1, path2 = u'添加IDC', u'资产管理', u'添加IDC'
    if request.method == 'POST':
        j_idc = request.POST.get('j_idc')
        j_comment = request.POST.get('j_comment')
        if IDCS.objects.filter(name=j_idc):
            emg = u'该IDC已存在!'
            return my_render('stor_idc/idc_add.html', locals(), request)
        else:
            user = request.session.get('user_id')
            msg_title=u'添加IDC'
            smg = u'IDC:%s 添加成功！' % j_idc
            IDCS.objects.create(name=j_idc, comment=j_comment)
            db_change_record(user=user,event_type='AI',event_title=msg_title,event_msg=smg,start_time=datetime.datetime.now())

    return my_render('stor_idc/idc_add.html', locals(), request)

def idc_list(request):
    """ 列出IDC """
    header_title, path1, path2 = u'查看IDC', u'资产管理', u'查看IDC'
    dept_id = get_user_dept(request)
    dept = DEPTS.objects.all()
    keyword = request.GET.get('keyword', '')
    if keyword:
        posts = IDCS.objects.filter(Q(name__contains=keyword) | Q(comment__contains=keyword))
    else:
        posts = IDCS.objects.exclude(name='ALL').order_by('id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('stor_idc/idc_list.html', locals(), request)

class AddError(Exception):
    pass

def build_add(request):
    header_title, path1, path2 = '添加楼号', '楼号管理', '添加楼号'
    if request.method == 'POST':
        name = request.POST.get('name', '')
        comment = request.POST.get('comment', '')

        try:
            if not name:
                raise AddError('楼号名称不能为空')
            if Builds.objects.filter(name=name):
                raise AddError(u'部门名称 %s 已存在' % name)
        except AddError, e:
            error = e
        else:
            Builds(name=name, comment=comment).save()
            user = request.session.get('user_id')
            msg_title=u'添加楼号'
            msg = u'Build: %s %s 添加成功！' % (name,comment)
            db_change_record(user=user,event_type='AB',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now())
    return render_to_response('stor_idc/build_add.html', locals(), context_instance=RequestContext(request))


def build_list(request):
    header_title, path1, path2 = '查看楼号', '楼号管理', '查看楼号'
    keyword = request.GET.get('search')
    if keyword:
        contact_list = Builds.objects.filter(Q(name__icontains=keyword) | Q(comment__icontains=keyword)).order_by('name')
    else:
        contact_list = Builds.objects.all().order_by('name')

    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(contact_list, request)

    return render_to_response('stor_idc/build_list.html', locals(), context_instance=RequestContext(request))

def db_add_floor(**kwargs):
    name = kwargs.get('name')
    group = Floors.objects.filter(name=name)
    #users = kwargs.pop('users')
    if group:
        raise AddError(u'楼层 %s 已经存在' % name)
    group = Floors(**kwargs)
    group.save()

def floor_add(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '添加楼层', '楼层管理', '添加楼层'
    ##user_all = Users.objects.all()
    #dept_all = DEPTS.objects.all()

    if request.method == 'POST':
        group_name = request.POST.get('group_name', '')
        #dept_id = request.POST.get('dept_id', '')
        #users_selected = request.POST.getlist('users_selected', '')
        comment = request.POST.get('comment', '')
        user_id = request.session.get('user_id')
        user = Users.objects.filter(id=user_id)
        try:
            if '' in [group_name, comment]:
                error = u'楼层 或 备注 不能为空'
                raise AddError(error)

            if Floors.objects.filter(name=group_name):
                error = u'楼层已存在'
                raise AddError(error)

            db_add_floor(name=group_name, comment=comment)
        except AddError:
            pass
        except TypeError:
            error = u'保存楼层信息失败'
        else:
            user = request.session.get('user_id')
            msg_title=u'添加楼层'
            msg = u'Floor: %s %s 添加成功！' % (group_name,comment)
            db_change_record(user=user,event_type='AF',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now())
    return render_to_response('stor_idc/floor_add.html', locals(), context_instance=RequestContext(request))

def floor_list(request):
    header_title, path1, path2 = '查看楼层', '楼层管理', '查看楼层'
    keyword = request.GET.get('search', '')
    did = request.GET.get('did', '')
    contact_list = Floors.objects.all().order_by('name')

    if did:
        dept = DEPTS.objects.filter(id=did)
        if dept:
            dept = dept[0]
            contact_list = dept.usergroup_set.all()

    if keyword:
        contact_list = contact_list.filter(Q(name__icontains=keyword) | Q(comment__icontains=keyword))

    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(contact_list, request)
    return render_to_response('stor_idc/floor_list.html', locals(), context_instance=RequestContext(request))

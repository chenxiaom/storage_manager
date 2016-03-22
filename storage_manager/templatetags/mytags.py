# coding: utf-8

import re
import ast
import time
from django import  template
from django.db.models import Sum
from storage_manager.models import *
from stor_info.models import *
from storage_manager.api import *

register = template.Library()

@register.filter(name='bool2str')
def bool2str(value):
    if value:
        return u'是'
    else:
        return u'否'

@register.filter(name='to_name')
def to_name(user_id):
    try:
        user = Users.objects.filter(id=int(user_id))
        if user:
            user = user[0]
            return user.username
    except:
        return '非法用户'

@register.filter(name='to_dept_name')
def to_dept_name(user_id):
    try:
        user = Users.objects.filter(id=int(user_id))
        if user:
            user = user[0]
            return user.dept.name
    except:
        return '非法部门'

@register.filter(name='get_role')
def get_role(user_id):
    user_role = {'SU': u'超级管理员', 'DA': u'部门管理员', 'CU': u'普通用户'}
    user = Users.objects.filter(id=user_id)
    if user:
        user = user[0]
        return user_role.get(str(user.role), u"普通用户")
    else:
        return u"普通用户"

@register.filter(name='to_role_name')
def to_role_name(role_id):
    role_dict = {'0': '普通用户', '1': '部门管理员', '2': '超级管理员'}
    return role_dict.get(str(role_id), '未知')

@register.filter(name='to_tb_space')
def to_tb_space(capacity):
    if capacity:
        capacity=float(capacity)/1000
        html='%s TB' %  capacity
    else:
        html='0 TB'
    return html

@register.filter(name='to_stor_sn')
def to_stor_sn(stor_sn_id):
    try:
        stor_sn = StorageInfos.objects.filter(id=stor_sn_id).values("stor_sn")
        #all_allocated_ldev_count = StorHosts.objects.filter(stor_sn_id=int(storinfo_id)).aggregate(Sum('host_ldev_count'))
        if stor_sn:
            stor_sn=stor_sn[0]
            #all_allocated_ldev_count.setdefault('host_ldev_count__sum','0')
            return stor_sn['stor_sn']
        else:
            return 0
    except:
        return '返回存储SN失败,非法存储ID'


#根据存储ID列出已分配给Host的容量
@register.filter(name='to_allocated_space')
def to_allca_cap(storinfo_id):
    try:
        all_allocated_space_count = StorHosts.objects.filter(stor_sn_id=int(storinfo_id)).aggregate(Sum('host_allocated_size'))
        if all_allocated_space_count['host_allocated_size__sum'] == None:
            return 0
        else:
            return all_allocated_space_count['host_allocated_size__sum']

    except:
        return '返回已分配给Host的Space失败，非法存储ID'

#根据存储ID列出已分配给Host的Ldevs
@register.filter(name='to_allocated_ldevs')
def to_allca_cap(storinfo_id):
    try:
        all_allocated_ldev_count = StorHosts.objects.filter(stor_sn_id=int(storinfo_id)).aggregate(Sum('host_ldev_count'))
        if all_allocated_ldev_count['host_ldev_count__sum'] == None :
            #all_allocated_ldev_count.setdefault('host_ldev_count__sum','0')
            #return all_allocated_ldev_count['host_ldev_count__sum']
            return 0
        else:
            return all_allocated_ldev_count['host_ldev_count__sum']
    except:
        return '返回已分配给Host的Ldevs失败，非法存储ID'

@register.filter(name='to_allocated_map_groups')
def to_allocated_map_groups(storinfo_id):
    try:
        mapgroups = StorHosts.objects.filter(stor_sn_id=storinfo_id).values("host_map").distinct().count()
        if mapgroups:
            return mapgroups
        else:
            return 0
    except:
        return '非法存储ID'


@register.filter(name='to_get_loc')
def to_get_loc(storinfo_id):
    try:
        stor_loc = StorLocation.objects.filter(stor_sn_id=storinfo_id).values()
        if stor_loc:
            stor_loc=stor_loc[0]
            stor_loc_idc=stor_loc['stor_idc_id']
            stor_loc_build=stor_loc['stor_build_id']
            stor_loc_floor=stor_loc['stor_floor_id']
            idc_name = IDCS.objects.filter()
            build_name = Builds.objects.filter()
            floor_name = Floors.objects.filter()

            html = "%s %s %s " % (stor_loc_idc,stor_loc_build,stor_loc_floor)
            return html
        else:
            return "None"
    except:
        return '非法存储ID'


@register.filter(name='get_remain_ldevs')
def get_remain_ldevs(stor_sn):
    try:
        stor_info = StorageInfos.objects.filter(stor_sn=stor_sn).values()
        if stor_info:
            stor_info=stor_info[0]
            #stor_sn=stor_info['stor_sn']
            stor_remain_ldevs=stor_info['stor_remain_ldevs']

            #html = "%s %s %s " % (stor_loc_idc,stor_loc_build,stor_loc_floor)
            return stor_remain_ldevs
        else:
            return "None"
    except:
        return '非法存储ID'

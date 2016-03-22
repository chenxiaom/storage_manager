# coding:utf-8
import json
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from storage_manager.api import *
from stor_info.models import *
from django.http import HttpResponseNotFound,HttpResponseRedirect,HttpResponse
# Create your views here.

class AddError(Exception):
    pass


def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))


def manu_list(request):
    """ 列出制造商 """
    header_title, path1, path2 = u'查看制造商', u'资产管理', u'查看制造商'
    keyword = request.GET.get('keyword', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    #user_id = get_session_user_info(request)[0]
    if keyword:
        post_keyword_all = Manufacturer.objects.filter(Q(name__contains=keyword) |
                                            Q(comment__contains=keyword)).distinct().order_by('name')
        posts = post_keyword_all
    else:
        post_all = Manufacturer.objects.all().order_by('name')
        posts = post_all
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('stor_info/manu_list.html', locals(), request)


def model_list(request):
    """ 列出型号 """
    header_title, path1, path2 = u'查看型号', u'资产管理', u'查看型号'
    keyword = request.GET.get('keyword', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    #user_id = get_session_user_info(request)[0]
    manu_id =  request.GET.get('manu_id', '')
    if manu_id:
        posts = StorModels.objects.filter(stor_manu_id=manu_id).order_by('model')
    if keyword:
        post_keyword_all = StorModels.objects.filter(Q(model__contains=keyword) |
                                            Q(comment__contains=keyword)).distinct().order_by('model')
        posts = post_keyword_all
    else:
        post_all = StorModels.objects.all().order_by('model')
        #posts = post_all
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('stor_info/model_list.html', locals(), request)


def manu_add(request):
    header_title, path1, path2 = '添加制造商', '制造商管理', '添加制造商'
    if request.method == 'POST':
        name = request.POST.get('name', '')
        comment = request.POST.get('comment', '')

        try:
            if not name:
                raise AddError('制造商名称不能为空')
            if Manufacturer.objects.filter(name=name):
                raise AddError(u'制造商 %s 已存在' % name)
        except AddError, e:
            error = e
        else:
            Manufacturer(name=name, comment=comment,date_joined=datetime.datetime.now()).save()
            user = request.session.get('user_id')
            msg_title=u'添加制造商'
            msg = u'Manufacturer: %s %s 添加成功！' % (name,comment)
            db_change_record(user=user,event_type='AMA',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now())
    return render_to_response('stor_info/manu_add.html', locals(), context_instance=RequestContext(request))


def model_add(request):
    header_title, path1, path2 = '添加存储型号', '存储型号管理', '添加存储型号'
    manuid = request.GET.get('j_manu_id', '')
    manu_list=Manufacturer.objects.filter(id=manuid)
    #manu_list=Manufacturer.objects.all()
    if request.method == 'POST':
        manu_id = request.POST.get('j_manu', '')
        name = request.POST.get('name', '')
        comment = request.POST.get('comment', '')
        #manuobj=Manufacturer.objects.filter(id=manu_id)
        #manu_name= manuobj.name
        #manu_id=int(manu_id)
        try:
            if not name:
                raise AddError('型号不能为空')
            if StorModels.objects.filter(model=name):
                raise AddError(u'型号 %s 已存在' % name)
        except AddError, e:
            error = e
        else:
            StorModels(model=name,stor_manu_id=manu_id,comment=comment,date_joined=datetime.datetime.now()).save()
            #StorModels(model='XXCXM',stor_manu=,comment='CCC',date_joined=datetime.datetime.now()).save()
            user = request.session.get('user_id')
            msg_title=u'添加型号'
            msg = u'Storage Model: %s %s 添加成功！' % (manu_id,name)
            db_change_record(user=user,event_type='AMO',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now())
    return render_to_response('stor_info/model_add.html', locals(), context_instance=RequestContext(request))


#添加存储的插入数据库的方法
def db_stor_insert(stor_info):
    """ 添加存储时数据库操作函数 """
    stor_name,stor_use,stor_model,stor_sn,stor_bare_cap, stor_space_cap, stor_ldevs_count, stor_cmdisk, stor_active, stor_comment = stor_info
    #idc = IDC.objects.filter(id=idc)
    a = StorageInfos(stor_name=stor_name,
                  stor_use=stor_use,
                  stor_model_id=int(stor_model),
                  stor_sn=stor_sn,
                  stor_bare_capacity=stor_bare_cap, stor_space_capacity=stor_space_cap,stor_ldevs_count=stor_ldevs_count,
                  stor_remain_capacity=stor_space_cap,stor_remain_ldevs=stor_ldevs_count,stor_idle_rage=float(100.00),
                  stor_cm_disk_host=stor_cmdisk,is_active=int(stor_active),comment=stor_comment,
                  date_joined=datetime.datetime.now(),is_delete=0)
    a.save()


#根据根据存储生产厂商获取型号
def manu_get_model(request):
    #stor_model = request.POST.get('j_stor_model')
    stor_manu = request.GET.get('j_stor_manu')
    if stor_manu =='' :
        stor_manu=  [{"stor_manu": "NULL", "id":"NULL"}]
        data = {'stor_manu':stor_manu}
        return HttpResponse(json.dumps(data,ensure_ascii=False))
    stor_lst = StorModels.objects.filter(stor_manu_id=stor_manu).values('id','model')
    stor_manu = []
    for stormanu in stor_lst:
        stor_manu.append(stormanu)
    data = {'stor_manu':stor_manu}
    #return HttpResponse(stor_sns)
    return HttpResponse(json.dumps(data,ensure_ascii=False))


def stor_add(request):
    """ 添加存储 """
    header_title, path1, path2 = u'添加存储', u'资产管理', u'添加存储'
    login_types = {'L': 'WEB-https', 'M': '远程桌面'}
    eidc = IDCS.objects.exclude(name='ALL')
    manu = Manufacturer.objects.exclude(name='ALL')
    emodel=StorModels.objects.exclude(model='ALL')

    if is_super_user(request):
        builds = Builds.objects.exclude(name='ALL')
        floors = Floors.objects.exclude(name='ALL')
        #egroup = BisGroup.objects.exclude(name='ALL')
    elif is_group_admin(request):
        dept = get_session_user_info(request)[5]
        egroup = dept.bisgroup_set.all()

    if request.method == 'POST':
        stor_name = request.POST.get('j_stor_name')
        stor_use = request.POST.get('j_stor_use')
        stor_model = request.POST.get('j_stor_model')
        stor_sn = request.POST.get('j_stor_sn')
        stor_bare_cap = request.POST.get('j_stor_bare_cap')
        stor_space_cap = request.POST.get('j_stor_space_cap')
        stor_ldevs_count = request.POST.get('j_stor_ldevs_count')
        stor_cmdisk = request.POST.get('j_stor_cmdisk')
        stor_active = request.POST.get('j_stor_active')
        stor_comment = request.POST.get('j_stor_comment')

        if int(stor_bare_cap) < int(stor_space_cap):
            emg = u'Warring: RAID后的容量:%s 不能大于裸容量 : %s !' % (stor_space_cap , stor_bare_cap)
            return my_render('stor_info/stor_add.html', locals(), request)
        if is_super_user(request):
            stor_info = [stor_name,stor_use,stor_model,stor_sn,stor_bare_cap, stor_space_cap, stor_ldevs_count, stor_cmdisk, stor_active, stor_comment]
        elif is_group_admin(request):
            stor_info = [stor_name,stor_use,stor_model,stor_sn,stor_bare_cap, stor_space_cap, stor_ldevs_count, stor_cmdisk, stor_active, stor_comment]

        if StorageInfos.objects.filter(stor_sn=str(stor_sn)):
            emg = u'Storage: %s %s 已存在!' % (stor_name,stor_sn)
            return my_render('stor_info/stor_add.html', locals(), request)
        else:
            db_stor_insert(stor_info)
        if StorageInfos.objects.filter(stor_sn=str(stor_sn)):
            smg = u'Storage: %s %s 添加成功!' % (stor_name,stor_sn)
            user = request.session.get('user_id')
            msg_title=u'添加存储'
            msg = u'Storage: %s %s 添加成功!' % (stor_name,stor_sn)
            db_change_record(user=user,event_type='AST',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now(),stor_sn=stor_sn)
        else:
            emg = u'Storage: %s %s 添加失败!' % (stor_name,stor_sn)
    return my_render('stor_info/stor_add.html', locals(), request)


def stor_list(request):
    """ 列出存储 """
    header_title, path1, path2 = u'查看存储', u'资产管理', u'查看存储'
    keyword = request.GET.get('keyword', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    #user_id = get_session_user_info(request)[0]
    if keyword:
        post_keyword_all = StorageInfos.objects.filter(Q(stor_name__contains=keyword) |
                                            Q(stor_sn__contains=keyword)).distinct().order_by('stor_model_id')
        posts = post_keyword_all
    else:
        post_all = StorageInfos.objects.all().order_by('stor_model_id')
        posts = post_all
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('stor_info/stor_list.html', locals(), request)

    #contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    #return my_render('stor_info/stor_list.html', locals(), request)
    #return render_to_response('stor_info/stor_list.html', locals(), context_instance=RequestContext(request))
    #return render(request,'stor_info/stor_list.html')


def stor_detail(request):
    """ 主机详情 """
    header_title, path1, path2 = u'存储详细信息', u'资产管理', u'存储详情'
    stor_id = request.GET.get('id', '')
    post = StorageInfos.objects.filter(id=stor_id)
    #post = StorageInfos.objects.filter(id=stor_id).values('stor_sn')
    if not post:
        return httperror(request, '没有此存储!')
    post = post[0]
    hostmaps=StorHosts.objects.filter(stor_sn_id=stor_id)
    log_all = Logs.objects.filter(stor_sn=post.stor_sn).order_by("-start_time")
    return my_render('stor_info/stor_detail.html', locals(), request)


#根据型号获取SN
def model_get_sn(request):
    #stor_model = request.POST.get('j_stor_model')
    stor_model = request.GET.get('j_stor_model')
    if stor_model =='' :
        stor_sns=  [{"stor_sn": "NULL", "id":"NULL"}]
        data = {'stor_sns':stor_sns}
        return HttpResponse(json.dumps(data,ensure_ascii=False))
    stor_lst = StorageInfos.objects.filter(stor_model=stor_model).values('id','stor_sn')
    stor_sns = []
    for storsn in stor_lst:
        stor_sns.append(storsn)
    data = {'stor_sns':stor_sns}
    #return HttpResponse(stor_sns)
    return HttpResponse(json.dumps(data,ensure_ascii=False))


#根据SN_id获取剩余容量和剩余的Ldevs
def snid_get_remain(request):
    #stor_model = request.POST.get('j_stor_id')
    stor_id = request.GET.get('j_stor_id')
    if stor_id =='' :
        remains=[{"stor_remain_capacity": 'NULL', "stor_remain_ldevs": 'NULL'}]
        return HttpResponse(json.dumps(remains,ensure_ascii=False))
    stor_remains = StorageInfos.objects.filter(id=stor_id).values('stor_remain_ldevs','stor_remain_capacity')
    remains = []
    for remain in stor_remains:
        remains.append(remain)
    #data = {'remain':remains}
    #return HttpResponse(stor_sns)
    return HttpResponse(json.dumps(remains,ensure_ascii=False))


#更新存储容量的方法
def update_stor_cap(new_stor_info,change_mark,stor_change_log_info,new_host_info):
    stor_sn, new_remain_ldevs, new_remain_space, new_idle_rage = new_stor_info
    user, host_map_id, host_map, stor_name, stor_remain_ldevs, stor_remain_capacity, stor_idle_rage = stor_change_log_info
    host_map_id, new_host_ldev_count, host_ldev_size, new_host_allocated_size = new_host_info
    stor_sn = str(stor_sn)
    stor_info = StorageInfos.objects.filter(stor_sn=stor_sn)
    if not stor_info:
        html= '更新存储容量失败，没有找到 %s 存储!' % stor_sn
        return httperror( new_stor_info ,html)
    stor_info = stor_info[0]
    modify_number = int(stor_info.modify_number)+1
    StorageInfos.objects.filter(stor_sn=stor_sn).update(stor_remain_ldevs=new_remain_ldevs,
                                                        stor_remain_capacity=new_remain_space,
                                                        stor_idle_rage=new_idle_rage,
                                                        modify_number=modify_number,
                                                        last_update=datetime.datetime.now())
    change_class=u'Change Storage'
    msg_title=u'更新存储信息成功.'
    if change_mark == 'Add':
        event_type='Add_Stor_Host'
        msg = u'Host Group[Add新增]: 存储序列号 %s , 主机组id为 %s , 主机组名称 %s , 新增容量 %s * %s GB = %s GB .' % (stor_sn,host_map_id, host_map,new_host_ldev_count, host_ldev_size, new_host_allocated_size )
    elif change_mark == 'Delete' :
        event_type='Del_Stor_Host'
        msg = u'Host Group[Delete删除]: 存储序列号 %s , 主机组id为 %s , 主机组名称 %s ,删除容量 %s * %s GB = %s GB .' % (stor_sn,host_map_id, host_map,new_host_ldev_count, host_ldev_size, new_host_allocated_size )
    elif change_mark == 'Increase' :
        event_type='Inc_Stor_Host'
        msg = u'Host Group[Increase扩容]: 存储序列号 %s , 主机组id为 %s , 主机组名称 %s ,扩容容量 %s * %s GB = %s GB .' % (stor_sn,host_map_id, host_map,new_host_ldev_count, host_ldev_size, new_host_allocated_size )
    elif change_mark == 'Decrease' :
        event_type='Dec_Stor_Host'
        msg = u'Host Group[Decrease回收]: 存储序列号 %s , 主机组id为 %s , 主机组名称 %s ,回收容量 %s * %s GB = %s GB .' % (stor_sn,host_map_id, host_map,new_host_ldev_count, host_ldev_size, new_host_allocated_size )

    db_change_record(user=user, event_type=event_type,event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now(),
                                change_class=change_class,stor_sn=stor_sn,host_map=host_map,
                                new_ldevs=new_remain_ldevs, last_ldevs=int(stor_remain_ldevs) ,
                                new_space=new_remain_space, last_space=int(stor_remain_capacity) ,
                                new_idle=new_idle_rage, last_idle=stor_idle_rage ,
                                event_inst=2)  #2是代表更新记录


#更新HostGroup容量的方法 用于回收和扩容后更新HostGroup信息
def update_host_cap(new_host_info,change_mark,change_log_info):
    host_map_id, new_host_ldev_count, host_ldev_size, new_host_allocated_size = new_host_info
    user, stor_sn, host_map,host_ldev_count, host_allocated_size, change_devs, host_ldev_size, change_allocated_size = change_log_info
    #stor_sn = str(stor_sn)
    host_info = StorageInfos.objects.filter(id=host_map_id)
    if not host_info:
        return httperror( new_host_info , '更新存储容量失败，没有找到此存储!')
    host_info = host_info[0]
    modify_number = int(host_info.modify_number)+1
    StorHosts.objects.filter(id=host_map_id).update(host_ldev_count=new_host_ldev_count,
                                                        host_allocated_size=new_host_allocated_size,
                                                        modify_number=modify_number,
                                                        last_update=datetime.datetime.now())
    #change_class=u'Change HostGroup'
    #msg_title=u'更新HostGroup信息成功'
    #if change_mark == 'Add':
    #    event_type='Add_Stor_Host'
    #    msg = u'Host Group[Add新增]:%s 划分 %s × %s GB = %s GB .' % (host_map,host_ldev_count,host_ldev_size, host_allocated_size)
    #elif change_mark == 'Delete' :
    #    event_type='Del_Stor_Host'
    #    msg = u'Host Group[Delete删除]:%s 删除(回收) %s × %s GB = %s GB .' % (host_map,host_ldev_count,host_ldev_size, host_allocated_size)
    #if change_mark == 'Increase' :
    #    event_type='Inc_Stor_Host'
    #    msg = u'Host Group[Increase扩容]: 存储序列号 %s , 主机组id为 %s , 主机组名称 %s ,扩容容量 %s * %s GB = %s GB .' % (stor_sn,host_map_id, host_map,host_ldev_count, host_ldev_size, host_allocated_size )
    #elif change_mark == 'Decrease' :
    #    event_type='Dec_Stor_Host'
    #    msg = u'Host Group[Decrease回收]: 存储序列号 %s , 主机组id为 %s , 主机组名称 %s ,回收容量 %s * %s GB = %s GB .' % (stor_sn,host_map_id, host_map,host_ldev_count, host_ldev_size, host_allocated_size )


    #db_change_record(user=user, event_type=event_type, event_title=msg_title,event_msg=msg, start_time=datetime.datetime.now(),
    #                            change_class=change_class,stor_sn=stor_sn,host_map=host_map,
    #                            new_ldevs=new_host_ldev_count, last_ldevs=int(host_ldev_count) ,
    #                            new_space=new_host_allocated_size, last_space=int(host_allocated_size) ,
    #                            event_inst=2)

def db_host_insert(host_info):
    """ 添加host时数据库操作函数 """
    stor_sn_id , host_map, host_ldev_count, host_ldev_size, host_allocated_size, host_active, comment = host_info
    #插入数据
    a = StorHosts(stor_sn_id=int(stor_sn_id), host_map=host_map,
                  host_ldev_count=int(host_ldev_count), host_ldev_size=int(host_ldev_size),
                  host_allocated_size=int(host_allocated_size),
                  host_active=host_active, comment=comment,
                  last_update=datetime.datetime.now(),
                  date_joined=datetime.datetime.now())
    a.save()


############################################################################################################
#更新存储容的方法，调用形式 update_stor_host_size(data,stor_sn_id,host_map_id,change_mark)
#host group 的 新增/删除/扩容/回收 的公共函数
def change_map(user,data,stor_info,host_info,host_map_id,change_mark,host_chang_info):
    stor_sn_id, host_map, host_ldev_count, host_ldev_size, host_allocated_size, host_active, comment=host_info
    stor_sn, stor_name, stor_space_capacity, stor_ldevs_count, stor_remain_capacity, stor_remain_ldevs, stor_idle_rage = stor_info
    stor_remain_ldevs, stor_remain_capacity ,host_ldev_count, host_ldev_size = data
    user=user
    if host_chang_info:
        change_devs,change_allocated_size=host_chang_info
    if not change_mark:
        return httperror( data , '更新存储容量失败，未获取到 change_mark 的值!')
    stor_info = StorageInfos.objects.filter(id=stor_sn_id)
    host_map_info = StorHosts.objects.filter(id=host_map_id)

    if change_mark == 'Add':    #新增map
        if host_info :
            if StorHosts.objects.filter(host_map=str(host_map),host_ldev_size=int(host_ldev_size)):
                emg = u'Host: Mapping已存在!，您可以修 %s 主机的Mapping清单!' % host_map
                return my_render('stor_info/host_add3.html', locals(), data)
            else:
                db_host_insert(host_info)
                if StorHosts.objects.filter(host_map=str(host_map),host_ldev_size=int(host_ldev_size)):
                    #msg_title=u'添加主机Mapping'
                    #msg = u'Host: %s 和存储 %s 的Mapping添加成功!' % (host_map,stor_sn)
                    #db_change_record(user=user,event_type='ASH',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now(),stor_sn=stor_sn,event_inst=1)

                    new_remain_ldevs = int(stor_remain_ldevs) - int(host_ldev_count)   #用存储可用的ldev减去分配给主机的ldev就是剩余的ldev个数
                    new_remain_space = int(stor_remain_capacity) - int(host_allocated_size)   #用存储剩余空间减去分配给主机的空间，就是最新的剩余的存储空间
                    new_idle_rage=(float(new_remain_space)/float(stor_space_capacity))*100 #计算空闲率
                    new_idle_rage="%.2f" % new_idle_rage
                    new_idle_rage=float(new_idle_rage)
                    new_stor_info=[stor_sn,new_remain_ldevs,new_remain_space,new_idle_rage]
                    stor_change_log_info=[user,host_map_id,host_map,stor_name,stor_remain_ldevs,stor_remain_capacity,stor_idle_rage]
                    new_host_info=[host_map_id, host_ldev_count, host_ldev_size, host_allocated_size]
                    update_stor_cap(new_stor_info, change_mark, stor_change_log_info, new_host_info)      #引用更新存储容量的方法


        else :
            return httperror( data , '新增 host map 失败，未获取到 host_info 的值!')

    elif change_mark == 'Delete' :     #删除map
        del_host_map = StorHosts.objects.filter(id=host_map_id)
        del_host_map.delete()
        if not StorHosts.objects.filter(id=host_map_id):
            #msg_title=u'删除主机Mapping'
            #msg = u'Host: %s 已从存储 %s 的 Mapping 关系内删除!' % (host_map,stor_sn)
            #db_change_record(user=user,event_type='DSH',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now(),stor_sn=stor_sn,event_inst=3)

            new_remain_ldevs = int(stor_remain_ldevs) + int(host_ldev_count)   #用存储可用的ldev加上分配给主机的ldev就是回收后的ldev个数
            new_remain_space = int(stor_remain_capacity) + int(host_allocated_size)   #用存储剩余空间加上分配给主机的空间，就是最新的剩余的存储空间
            new_idle_rage=(float(new_remain_space)/float(stor_space_capacity))*100 #计算空闲率
            new_idle_rage="%.2f" % new_idle_rage
            new_idle_rage=float(new_idle_rage)
            new_stor_info=[stor_sn,new_remain_ldevs,new_remain_space,new_idle_rage]
            stor_change_log_info=[user,host_map_id,host_map,stor_name,stor_remain_ldevs,stor_remain_capacity,stor_idle_rage]
            new_host_info = [host_map_id, host_ldev_count, host_ldev_size, host_allocated_size]
            update_stor_cap(new_stor_info, change_mark, stor_change_log_info, new_host_info)      #引用更新存储容量的方法

            #msg_title=u'更新存储信息成功'
            #msg = u'删除(回收)Host Group:%s / Ldevs:%s 个 / Ldev Size:%s GB / Allocated Size: %s GB !' % (host_map,host_ldev_count,host_ldev_size, host_allocated_size)
            #db_change_record(user=user, event_type='ASH',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now(),stor_sn=stor_sn,
            #            new_ldevs=new_remain_ldevs, last_ldevs=int(stor_remain_ldevs) ,
            #            new_space=new_remain_space, last_space=int(stor_remain_capacity) ,
            #            new_idle=new_idle_rage, last_idle=stor_idle_rage ,
            #            event_inst=2)  #2是代表更新记录
        #host_map_info = StorHosts.objects.filter(id=host_map_id)
        #判断map是否存在，如果不存在，则更新storinfo

    elif change_mark == 'Increase' :    #增加map  扩容  host+   disk-
        print change_mark

        new_remain_ldevs = int(stor_remain_ldevs) - int(change_devs)   #用存储可用的ldev减去分配给主机的ldev就是剩余的ldev个数
        new_remain_space = int(stor_remain_capacity) - int(change_allocated_size)   #用存储剩余空间减去分配给主机的空间，就是最新的剩余的存储空间
        new_idle_rage=(float(new_remain_space)/float(stor_space_capacity))*100 #计算空闲率
        new_idle_rage="%.2f" % new_idle_rage
        new_idle_rage=float(new_idle_rage)
        new_stor_info=[stor_sn,new_remain_ldevs,new_remain_space,new_idle_rage]
        stor_change_log_info=[user,host_map_id,host_map,stor_name,stor_remain_ldevs,stor_remain_capacity,stor_idle_rage]

        new_host_ldev_count= int(host_ldev_count) + int(change_devs)
        new_host_allocated_size=int(host_allocated_size) + int(change_allocated_size)

        #new_host_info=[host_map_id,new_host_devs,new_host_count]
        change_host_info=[host_map_id, change_devs, host_ldev_size, change_allocated_size]
        update_stor_cap(new_stor_info, change_mark, stor_change_log_info, change_host_info)      #引用更新存储容量的方法

        new_host_info = [host_map_id, new_host_ldev_count, host_ldev_size, new_host_allocated_size]
        change_log_info=[user, stor_sn, host_map,host_ldev_count, host_allocated_size, change_devs, host_ldev_size, change_allocated_size]
        update_host_cap(new_host_info,change_mark,change_log_info)



    elif change_mark == 'Decrease' :    #减少map  回收  host-   disk+
        print change_mark
        new_remain_ldevs = int(stor_remain_ldevs) + int(change_devs)   #用存储可用的ldev减去分配给主机的ldev就是剩余的ldev个数
        new_remain_space = int(stor_remain_capacity) + int(change_allocated_size)   #用存储剩余空间减去分配给主机的空间，就是最新的剩余的存储空间
        new_idle_rage=(float(new_remain_space)/float(stor_space_capacity))*100 #计算空闲率
        new_idle_rage="%.2f" % new_idle_rage
        new_idle_rage=float(new_idle_rage)
        new_stor_info=[stor_sn,new_remain_ldevs,new_remain_space,new_idle_rage]
        stor_change_log_info=[user,host_map_id,host_map,stor_name,stor_remain_ldevs,stor_remain_capacity,stor_idle_rage]

        new_host_ldev_count= int(host_ldev_count) - int(change_devs)
        new_host_allocated_size=int(host_allocated_size) - int(change_allocated_size)

        change_host_info=[host_map_id, change_devs, host_ldev_size, change_allocated_size]
        update_stor_cap(new_stor_info, change_mark, stor_change_log_info, change_host_info)      #引用更新存储容量的方法

        change_log_info=[user, stor_sn, host_map,host_ldev_count, host_allocated_size, change_devs, host_ldev_size, change_allocated_size]
        new_host_info = [host_map_id, new_host_ldev_count, host_ldev_size, new_host_allocated_size]
        update_host_cap(new_host_info,change_mark,change_log_info)

#添加Mapping主机
def host_add4(request):
    """ 添加Mapping主机 """
    header_title, path1, path2 = u'添加Mapping主机', u'资产管理', u'添加主机'
    emodel = StorModels.objects.exclude(model='ALL')
    stor_sn_id = request.GET.get('stor_sn_id')
    stor_info = StorageInfos.objects.filter(id=stor_sn_id)
    if not stor_info:
        return httperror(request, '没有此存储!')
    stor_info = stor_info[0]

    if request.method == 'POST':
        stor_sn_id = request.POST.get('j_stor_sn')
        host_map = request.POST.get('j_host_map')
        host_ldev_count = request.POST.get('j_host_ldev_count')
        host_ldev_size = request.POST.get('j_host_ldev_size')
        host_allocated_size = request.POST.get('j_host_allocated_size')
        host_active = request.POST.get('j_host_active')
        if not host_active :
            host_active=0
        comment = request.POST.get('j_stor_comment')

        stor_info = StorageInfos.objects.filter(id=stor_sn_id)
        if not stor_info:
            return httperror(request, '没有此存储!')
        stor_info = stor_info[0]
        stor_sn = stor_info.stor_sn   #根据stor_sn_id找出的存储信息，从存储信息中找到该存储的序列号
        stor_name = stor_info.stor_name
        stor_space_capacity = stor_info.stor_space_capacity
        stor_ldevs_count = stor_info.stor_ldevs_count
        stor_remain_capacity = stor_info.stor_remain_capacity
        stor_remain_ldevs = stor_info.stor_remain_ldevs
        stor_idle_rage = stor_info.stor_idle_rage
        stor_info = [stor_sn,stor_name, stor_space_capacity , stor_ldevs_count,
                     stor_remain_capacity, stor_remain_ldevs, stor_idle_rage]

        host_info = [stor_sn_id, host_map, host_ldev_count, host_ldev_size, host_allocated_size, host_active, comment]

        data = [stor_remain_ldevs,  stor_remain_capacity ,host_ldev_count, host_ldev_size]

        if StorHosts.objects.filter(host_map=str(host_map),host_ldev_size=int(host_ldev_size)):
            emg = u'Host: Mapping已存在!，您可以修 %s 主机的Mapping清单!' % host_map
            return my_render('stor_info/host_add3.html', locals(), request)
        else:
            change_mark='Add'
            host_chang_info=''
            user = request.session.get('user_id')
            host_map_id=1
            change_map(user,data,stor_info,host_info,host_map_id,change_mark,host_chang_info)
            if StorHosts.objects.filter(host_map=str(host_map),host_ldev_size=int(host_ldev_size)):
                smg = u'Host: %s 新增 %s 和存储 %s 的Mapping添加成功!' % (user,host_map,stor_sn)
            else:
                emg = u'Host: %s 和存储 %s 的Mapping添加失败!' % (host_map,stor_sn)
    return my_render('stor_info/host_add4.html', locals(), request)

def host_del_map(request):
    host_map_id = request.GET.get('map_id')

    host_info=StorHosts.objects.filter(id=host_map_id)
    host_info = host_info[0]

    host_map_id = host_info.id

    stor_sn_id = host_info.stor_sn_id
    host_map= host_info.host_map
    host_ldev_count= host_info.host_ldev_count
    host_ldev_size= host_info.host_ldev_size
    host_allocated_size= host_info.host_allocated_size
    host_active= host_info.host_active
    comment= host_info.comment
    host_info=[ stor_sn_id, host_map, host_ldev_count, host_ldev_size, host_allocated_size, host_active, comment ]

    stor_info = StorageInfos.objects.filter(id=stor_sn_id)
    stor_info = stor_info[0]
    stor_sn = stor_info.stor_sn   #根据stor_sn_id找出的存储信息，从存储信息中找到该存储的序列号
    stor_name = stor_info.stor_name
    stor_space_capacity = stor_info.stor_space_capacity
    stor_ldevs_count = stor_info.stor_ldevs_count
    stor_remain_capacity = stor_info.stor_remain_capacity
    stor_remain_ldevs = stor_info.stor_remain_ldevs
    stor_idle_rage = stor_info.stor_idle_rage
    stor_info = [stor_sn,stor_name, stor_space_capacity , stor_ldevs_count,
                 stor_remain_capacity, stor_remain_ldevs, stor_idle_rage]

    data=[stor_remain_ldevs,  stor_remain_capacity ,host_ldev_count, host_ldev_size]
    user = request.session.get('user_id')
    change_mark='Delete'
    host_chang_info=''
    change_map(user,data,stor_info,host_info,host_map_id,change_mark,host_chang_info)
    if StorHosts.objects.filter(id=host_map_id):
        #emg = u'Host: %s 新增 %s 和存储 %s 的Mapping删除失败!' % (user,host_map,stor_sn)
        #url='/stor_info/stor_detail/?id=%s' % stor_sn_id
        #return HttpResponseRedirect(url)
        html='error!'
        return HttpResponse(html)
    else:
        #smg = u'Host: %s 和存储 %s 的Mapping成功删除!' % (host_map,stor_sn)
        #url='/stor_info/stor_detail/?id=%s' % stor_sn_id
        #return HttpResponseRedirect(url)
        #return my_render('stor_info/stor_detail.html', locals(), request)
        html='success!'
        return HttpResponse(html)

def host_update(request):
    #扩容或回收的html页面函数
    #通过前端html的 扩容/回收字段判断是扩容还是回收
    #再根据接收到的数据进行相加或相减
    host_id = request.GET.get('id')
    hosts = StorHosts.objects.filter(id=host_id)
    if hosts:
        hosts=hosts[0]
        if request.method == 'POST':
            host_map_id = request.POST.get('j_host_map_id')
            change_mark = request.POST.get('j_change_mark')
            change_devs = request.POST.get('j_change_devs')
            #host_ldev_size = request.POST.get('j_host_ldev_size')
            change_allocated_size = request.POST.get('j_change_allocated_size')
            #dis_change = request.POST.get('j_dis_change')
            stor_sn_id = request.POST.get('j_stor_sn_id')

            stor_info = StorageInfos.objects.filter(id=stor_sn_id)
            if not stor_info:
                return httperror(request,'没有此存储 %s !' )
            stor_info = stor_info[0]
            stor_sn = stor_info.stor_sn   #根据stor_sn_id找出的存储信息，从存储信息中找到该存储的序列号
            stor_name = stor_info.stor_name
            stor_space_capacity = stor_info.stor_space_capacity
            stor_ldevs_count = stor_info.stor_ldevs_count
            stor_remain_capacity = stor_info.stor_remain_capacity
            stor_remain_ldevs = stor_info.stor_remain_ldevs
            stor_idle_rage = stor_info.stor_idle_rage
            stor_info = [stor_sn,stor_name, stor_space_capacity , stor_ldevs_count,
                         stor_remain_capacity, stor_remain_ldevs, stor_idle_rage]

            host_info = StorHosts.objects.filter(id=host_map_id)
            if not host_info:
                return httperror(request, '没有此HostGroup!')
            host_info =  host_info[0]
            host_map = host_info.host_map
            host_ldev_count = host_info.host_ldev_count
            host_ldev_size = host_info.host_ldev_size
            host_allocated_size = host_info.host_allocated_size
            host_active = host_info.host_active
            comment = host_info.comment
            host_info = [stor_sn_id, host_map, host_ldev_count, host_ldev_size, host_allocated_size, host_active, comment]
            host_chang_info=change_devs,change_allocated_size

            data = [stor_remain_ldevs,  stor_remain_capacity ,host_ldev_count, host_ldev_size]

            user = request.session.get('user_id')
            #host_map_id=1
            #host_chang_info=''
            change_map(user,data,stor_info,host_info,host_map_id,change_mark,host_chang_info)

            if StorHosts.objects.filter(host_map=str(host_map),host_ldev_size=int(host_ldev_size)):
                smg = u'Host: %s 新增 %s 和存储 %s 的Mapping添加成功!' % (user,host_map,stor_sn)
            else:
                emg = u'Host: %s 和存储 %s 的Mapping添加失败!' % (host_map,stor_sn)
        return render_to_response('stor_info/host_update.html', locals(), context_instance=RequestContext(request))

    else:
        #return httperror(request, '该Host Id 不存在!')
        emg=u'该Host Id: %s 不存在!' % host_id
        #return httperror(request, '更新存储容量失败，没有找到此存储!')
        return render_to_response('stor_info/host_update.html', locals(), context_instance=RequestContext(request))





############################################################################################################



def host_list(request):
    """ 列出Host Mapping Groups """
    header_title, path1, path2 = u'主机存储Mapping关系', u'资产管理', u'Host Mapping Groups'
    keyword = request.GET.get('keyword', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]
    if keyword:
        post_keyword_all = StorHosts.objects.filter(Q(host_map__contains=keyword))
        posts = post_keyword_all
    else:
        post_all = StorHosts.objects.all().order_by('host_map')
        posts = post_all
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('stor_info/host_list.html', locals(), request)

def host_detail(request):
    host_id = request.GET.get('id')
    hosts = StorHosts.objects.filter(id=host_id)
    if hosts:
        hosts=hosts[0]
        #emg=u'该Host Id 不存在!'
        #return httperror(request, '更新存储容量失败，没有找到此存储!')
        return render_to_response('stor_info/host_detail.html', locals(), context_instance=RequestContext(request))

    else:
        #return httperror(request, '该Host Id 不存在!')
        emg=u'该Host Id: %s 不存在!' % host_id
        #return httperror(request, '更新存储容量失败，没有找到此存储!')
        return render_to_response('stor_info/host_detail.html', locals(), context_instance=RequestContext(request))



def stor_loc_list(request):
    """ 列出存储 """
    header_title, path1, path2 = u'查看存储', u'资产管理', u'查看存储'
    keyword = request.GET.get('keyword', '')
    did = request.GET.get('did', '')
    gid = request.GET.get('gid', '')
    sid = request.GET.get('sid', '')
    user_id = get_session_user_info(request)[0]
    if keyword:
        post_keyword_all = StorageInfos.objects.filter(Q(stor_name__contains=keyword) |
                                            Q(stor_sn__contains=keyword)).distinct().order_by('stor_model_id')
        posts = post_keyword_all
    else:
        post_all = StorageInfos.objects.all().order_by('stor_model_id')
        posts = post_all
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('stor_info/stor_loc_list.html', locals(), request)


def db_stor_loc(stor_loc_info):
    """ 添加存储时数据库操作函数 """
    stor_sn_id,idc_id,build_id,floor_id,comment = stor_loc_info
    #插入数据
    a = StorLocation(stor_sn_id=int(stor_sn_id),
                  stor_idc_id=idc_id,stor_build_id=build_id,stor_floor_id=floor_id,comment=comment,
                  date_joined=datetime.datetime.now())
    a.save()


def stor_mod_loc(request):
    manu = Manufacturer.objects.exclude(name='ALL')
    #emodel = StorModels.objects.exclude(model='ALL')
    eidc=IDCS.objects.exclude(name='ALL')
    builds=Builds.objects.exclude(name='ALL')
    floors=Floors.objects.exclude(name='ALL')

    if request.method == 'POST':
        stor_sn_id = request.POST.get('j_stor_sn')
        idc_id = request.POST.get('j_idc')
        build_id = request.POST.get('j_build')
        floor_id = request.POST.get('j_floor')
        comment = request.POST.get('j_comment')

        stor_loc_info=[stor_sn_id,idc_id,build_id,floor_id,comment]

        storinfo=StorageInfos.objects.filter(id=stor_sn_id)
        storinfo=storinfo[0]
        stor_sn=storinfo.stor_sn
        if StorLocation.objects.filter(stor_sn_id=stor_sn_id):
            emg = u'Location: 存储位置已存在!，您可以修 %s 存储的位置!' % stor_sn
            return my_render('stor_info/stor_mod_loc.html', locals(), request)
        else:
            db_stor_loc(stor_loc_info)
            storloc = StorLocation.objects.filter(stor_sn_id=stor_sn_id)
            if storloc:
                storloc=storloc[0]
                idc=storloc.stor_idc
                build=storloc.stor_build
                floor=storloc.stor_floor
                smg = u'Location: %s 存储的位置设定在： %s 机房 %s 号楼 %s 楼!' % (stor_sn,idc,build,floor)
                user = request.session.get('user_id')
                msg_title=u'设置存储位置'
                msg = u'Location: %s 存储的位置设定在： %s 机房 %s 号楼 %s 楼!' % (stor_sn,idc,build,floor)
                db_change_record(user=user,event_type='ASL',event_title=msg_title,event_msg=msg,start_time=datetime.datetime.now(),stor_sn=stor_sn,event_inst=1)
            else:
                emg = u'Location: %s 存储的位置设定失败!' %  stor_sn
    return my_render('stor_info/stor_mod_loc.html', locals(), request)




def wb_mod(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '更新维保', '存储维保管理', '更新维保'



def cabc_mod(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '更新CA/BC许可', '存储CA/BC管理', '更新CA/BC许可'




def login_mod(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '管理方式', '存储登录方式管理', '管理方式'

# -*- coding: utf-8 -*-
#from stor_idc.models import User
#from stor_info.models import Asset
from storage_manager.api import *
from storage_manager.models import Users
from stor_info.models import *


def name_proc(request):
    user_id = request.session.get('user_id')
    role_id = request.session.get('role_id')
    #if role_id == 2:
    user_total_num = Users.objects.all().count()
    stor_total_num = StorageInfos.objects.all().count()
    host_total_num = StorHosts.objects.values("host_map").distinct().count()
    idc_total_num = IDCS.objects.all().count()
    build_total_num = Builds.objects.all().count()
    floor_total_num = Floors.objects.all().count()

    manu_all_num = Manufacturer.objects.all().count()
    model_all_nm = StorModels.objects.all().count()

    #username = Users.objects.get(id=user_id).name
    #apply_info = Apply.objects.filter(admin=username, status=0, read=0)
    request.session.set_expiry(3600)

    info_dic = {'session_user_id': user_id,
                'session_role_id': role_id,
                'user_total_num': user_total_num,
                #'user_active_num': user_active_num,
                'stor_total_num': stor_total_num,
                'host_total_num': host_total_num,
                'idc_total_num' : idc_total_num,
                'build_total_num' : build_total_num,
                'floor_total_num' : floor_total_num,
                'manu_all_num':manu_all_num,
                'model_all_nm':model_all_nm,
                #'apply_info': apply_info}
                }

    return info_dic


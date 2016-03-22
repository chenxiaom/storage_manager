# -*- coding: utf-8 -*-
from django.db import models

class Logs(models.Model):
    user = models.CharField(max_length=20, null=True)
    event_inst=models.IntegerField(default=0)   #Log操作类型，0是info，1是insert，2是modify，3是delete
    change_class =  models.CharField(max_length=30, default='NONE')
    stor_sn = models.CharField(max_length=50, default='NONE')
    host_map = models.CharField(max_length=50, default='NONE')
    event_type = models.CharField(max_length=16, null=True)
    event_title = models.CharField(max_length=15, null=True)
    event_msg = models.CharField(max_length=520, null=True)
    start_time = models.CharField(max_length=120, null=True)
    new_ldevs=models.IntegerField(null=True)
    last_ldevs=models.IntegerField(null=True)
    new_space=models.IntegerField(null=True)
    last_space=models.IntegerField(null=True)
    new_idle=models.CharField(max_length=15, null=True)
    last_idle=models.CharField(max_length=15, null=True)
    #last_idle=models.DecimalField(max_digits=4,decimal_places=3, null=True)

    def __unicode__(self):
        return self.event_title


class Alert(models.Model):
    msg = models.CharField(max_length=20)
    time = models.DateTimeField(null=True)
    is_finished = models.BigIntegerField(default=False)
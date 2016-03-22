# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stor_log', '0003_logs_stor_sn'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='event_inst',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logs',
            name='last_idle',
            field=models.DecimalField(default=0.0, max_digits=4, decimal_places=3),
        ),
        migrations.AddField(
            model_name='logs',
            name='last_ldevs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logs',
            name='last_space',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logs',
            name='new_idle',
            field=models.DecimalField(default=0.0, max_digits=4, decimal_places=3),
        ),
        migrations.AddField(
            model_name='logs',
            name='new_ldevs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logs',
            name='new_space',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='logs',
            name='start_time',
            field=models.CharField(max_length=120, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stor_log', '0006_auto_20150912_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='last_idle',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='logs',
            name='new_idle',
            field=models.CharField(max_length=15, null=True),
        ),
    ]

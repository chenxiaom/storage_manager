# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stor_log', '0009_logs_change_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='host_map',
            field=models.CharField(default=b'NONE', max_length=50),
        ),
    ]

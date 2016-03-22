# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stor_log', '0002_auto_20150910_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='stor_sn',
            field=models.CharField(default=b'NONE', max_length=50),
        ),
    ]

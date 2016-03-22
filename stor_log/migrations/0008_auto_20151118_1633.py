# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stor_log', '0007_auto_20150912_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='event_type',
            field=models.CharField(max_length=16, null=True),
        ),
    ]

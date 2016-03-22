# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stor_log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='event_type',
            field=models.CharField(max_length=6, null=True),
        ),
    ]

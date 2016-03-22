# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stor_log', '0008_auto_20151118_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='change_class',
            field=models.CharField(default=b'NONE', max_length=30),
        ),
    ]

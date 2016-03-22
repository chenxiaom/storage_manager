# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stor_log', '0004_auto_20150912_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='last_idle',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='logs',
            name='last_ldevs',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='logs',
            name='last_space',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='logs',
            name='new_idle',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='logs',
            name='new_ldevs',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='logs',
            name='new_space',
            field=models.IntegerField(null=True),
        ),
    ]

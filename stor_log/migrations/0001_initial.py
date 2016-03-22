# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg', models.CharField(max_length=20)),
                ('time', models.DateTimeField(null=True)),
                ('is_finished', models.BigIntegerField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=20, null=True)),
                ('event_type', models.CharField(max_length=2, null=True)),
                ('event_title', models.CharField(max_length=15, null=True)),
                ('event_msg', models.CharField(max_length=120, null=True)),
                ('start_time', models.DateTimeField(null=True)),
            ],
        ),
    ]

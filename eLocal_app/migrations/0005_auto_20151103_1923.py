# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eLocal_app', '0004_auto_20151103_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenHour',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('day', models.CharField(max_length=9)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('closed', models.BooleanField()),
                ('store', models.ForeignKey(to='eLocal_app.Store')),
            ],
        ),
        migrations.RemoveField(
            model_name='openhours',
            name='store',
        ),
        migrations.DeleteModel(
            name='OpenHours',
        ),
    ]

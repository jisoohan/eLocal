# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eLocal_app', '0005_auto_20151103_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='city',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='store',
            name='country',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='store',
            name='zip_code',
            field=models.CharField(max_length=5),
        ),
    ]

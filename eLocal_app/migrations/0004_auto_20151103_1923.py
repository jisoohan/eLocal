# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eLocal_app', '0003_auto_20151103_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='city',
            field=models.CharField(max_length=128, default='Berkeley'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='country',
            field=models.CharField(max_length=128, default='USA'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='has_card',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='zip_code',
            field=models.CharField(max_length=10, default=94720),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='store',
            name='state',
            field=models.CharField(max_length=2),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eLocal_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openhours',
            name='weekday',
            field=models.IntegerField(choices=[(0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')]),
        ),
    ]

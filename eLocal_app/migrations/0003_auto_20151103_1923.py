# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eLocal_app', '0002_auto_20151103_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='store',
            name='longitude',
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default='Default description', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='state',
            field=models.IntegerField(default=4, choices=[(0, 'AL'), (1, 'AK'), (2, 'AZ'), (3, 'AR'), (4, 'CA'), (5, 'CO'), (6, 'CT'), (7, 'DE'), (8, 'FL'), (9, 'GA'), (10, 'HI'), (11, 'ID'), (12, 'IL'), (13, 'IN'), (14, 'IA'), (15, 'KS'), (16, 'KY'), (17, 'LA'), (18, 'ME'), (19, 'MD'), (20, 'MA'), (21, 'MI'), (22, 'MN'), (23, 'MS'), (24, 'MO'), (25, 'MT'), (26, 'NE'), (27, 'NV'), (28, 'NH'), (29, 'NJ'), (30, 'NM'), (31, 'NY'), (32, 'NC'), (33, 'ND'), (34, 'OH'), (35, 'OK'), (36, 'OR'), (37, 'PA'), (38, 'RI'), (39, 'SC'), (40, 'SD'), (41, 'TN'), (42, 'TX'), (43, 'UT'), (44, 'VT'), (45, 'VA'), (46, 'WA'), (47, 'WV'), (48, 'WI'), (49, 'WY'), (50, 'DC')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]

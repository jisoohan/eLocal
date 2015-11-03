# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpenHours',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')])),
                ('is_open', models.BooleanField()),
                ('from_hour', models.TimeField()),
                ('to_hour', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('items', models.ManyToManyField(through='eLocal_app.Inventory', to='eLocal_app.Item')),
            ],
        ),
        migrations.AddField(
            model_name='openhours',
            name='store',
            field=models.ForeignKey(to='eLocal_app.Store'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='item',
            field=models.ForeignKey(to='eLocal_app.Item'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='store',
            field=models.ForeignKey(to='eLocal_app.Store'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 14:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20171108_1347'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='hacker',
            unique_together=set([]),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-25 21:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0002_travels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='email',
        ),
    ]
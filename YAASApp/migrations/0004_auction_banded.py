# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-10-20 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YAASApp', '0003_auction_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='banded',
            field=models.TextField(default=b''),
        ),
    ]

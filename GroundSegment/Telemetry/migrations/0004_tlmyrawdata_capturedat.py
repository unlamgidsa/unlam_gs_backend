# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-13 11:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0003_auto_20180612_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlmyrawdata',
            name='capturedAt',
            field=models.DateTimeField(default=datetime.datetime(1900, 1, 1, 0, 0)),
        ),
    ]

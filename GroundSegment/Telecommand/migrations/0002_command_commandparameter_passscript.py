# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-12 13:00
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Telecommand', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('executeAt', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0, tzinfo=utc))),
                ('sent', models.DateTimeField(null=True)),
                ('executed', models.DateTimeField(null=True)),
                ('state', models.IntegerField(choices=[(0, 'Pending'), (1, 'Sent'), (2, 'Failed'), (3, 'Executed'), (4, 'Expirated')], default=0)),
                ('retry', models.IntegerField(default=0)),
                ('expiration', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0, tzinfo=utc))),
                ('binarycmd', models.BinaryField(null=True, verbose_name='Comando en formato binario listo para ser enviado por TCP/IP')),
                ('commandType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='Telecommand.CommandType')),
                ('satellite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='GroundSegment.Satellite')),
            ],
        ),
        migrations.CreateModel(
            name='CommandParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(default='', max_length=5)),
                ('command', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='Telecommand.Command')),
            ],
        ),
        migrations.CreateModel(
            name='PassScript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('script', models.TextField(default='Poner inclusion de django aca', help_text='Codifique el scripts', max_length=5120)),
                ('applied', models.BooleanField(default=False)),
                ('apass', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passScripts', to='GroundSegment.Pasada')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passScripts', to=settings.AUTH_USER_MODEL)),
                ('satellite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passScripts', to='GroundSegment.Satellite')),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-12 12:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GroundSegment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Codigo del tipo de comando', max_length=24, unique=True, verbose_name='Codigo del tipo de comando')),
                ('description', models.CharField(help_text='Decripcion del tipo de comando', max_length=100, unique=True, verbose_name='Decripcion del tipo de comando')),
                ('active', models.BooleanField(default=True)),
                ('transactional', models.BooleanField(default=False)),
                ('timeout', models.IntegerField(default=0, verbose_name='Tiempo en segundos?')),
                ('notes', models.TextField(max_length=512, null=True, verbose_name='Consecuencias, restricciones del comando')),
                ('maxRetry', models.IntegerField(default=2)),
                ('commandCode', models.CharField(default='0', max_length=24, verbose_name='Codigo de comando segun el satelite, por ejemplo para isis cubesat telemetryEPS->23')),
                ('satellite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandsType', to='GroundSegment.Satellite')),
                ('satelliteStates', models.ManyToManyField(related_name='commandsType', to='GroundSegment.SatelliteState')),
            ],
        ),
        migrations.CreateModel(
            name='CommandTypeParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='NoDet', help_text='Codigo del parametro', max_length=24, verbose_name='Codigo del parametro')),
                ('description', models.CharField(default='NoDet', help_text='Decripcion del satelite', max_length=100, verbose_name='Decripcion del parametro')),
                ('position', models.IntegerField(default=0)),
                ('valueMin', models.FloatField(default=0.0)),
                ('valueMax', models.FloatField(default=0.0)),
                ('commandType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='Telecommand.CommandType')),
            ],
        ),
    ]
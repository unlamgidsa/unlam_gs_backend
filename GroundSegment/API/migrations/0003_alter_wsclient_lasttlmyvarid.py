# Generated by Django 4.0.6 on 2023-02-16 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_wsclient_lasttlmyvarid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wsclient',
            name='lastTlmyVarId',
            field=models.BigIntegerField(default=-1),
        ),
    ]

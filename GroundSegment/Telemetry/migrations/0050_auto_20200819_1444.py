# Generated by Django 2.2.2 on 2020-08-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0049_auto_20200724_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlmyvar',
            name='rawValue',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tlmyvartype',
            name='lastCalIValue',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tlmyvartype',
            name='lastRawValue',
            field=models.BigIntegerField(default=0),
        ),
    ]

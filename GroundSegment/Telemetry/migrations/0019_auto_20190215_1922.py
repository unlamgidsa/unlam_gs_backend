# Generated by Django 2.0.7 on 2019-02-15 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0018_auto_20190215_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bltlmyvar',
            name='avrBValue',
        ),
        migrations.RemoveField(
            model_name='bltlmyvar',
            name='avrIValue',
        ),
        migrations.RemoveField(
            model_name='bltlmyvar',
            name='avrSValue',
        ),
        migrations.RemoveField(
            model_name='bltlmyvar',
            name='maxBValue',
        ),
        migrations.RemoveField(
            model_name='bltlmyvar',
            name='maxIValue',
        ),
        migrations.RemoveField(
            model_name='bltlmyvar',
            name='maxSValue',
        ),
        migrations.RemoveField(
            model_name='bltlmyvar',
            name='minBValue',
        ),
        migrations.RemoveField(
            model_name='bltlmyvar',
            name='minIValue',
        ),
        migrations.RemoveField(
            model_name='bltlmyvar',
            name='minSValue',
        ),
    ]

# Generated by Django 2.2.2 on 2020-07-15 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0047_tlmyvar_satellite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tlmyvar',
            name='satellite',
        ),
    ]

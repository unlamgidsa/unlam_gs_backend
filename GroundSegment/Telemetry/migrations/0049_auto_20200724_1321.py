# Generated by Django 2.2.2 on 2020-07-24 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0048_remove_tlmyvar_satellite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlmyvar',
            name='UnixTimeStamp',
            field=models.FloatField(default=0.0),
        ),
    ]
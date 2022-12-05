# Generated by Django 2.2.1 on 2019-05-28 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0003_auto_20190521_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='tle',
            name='validFrom',
            field=models.DateTimeField(null=True, verbose_name='Fecha inicio desde donde aplicar TLE'),
        ),
        migrations.AddField(
            model_name='tle',
            name='validUntil',
            field=models.DateTimeField(null=True, verbose_name='Fecha hasta desde donde aplicar TLE'),
        ),
    ]

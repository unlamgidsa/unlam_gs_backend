# Generated by Django 2.2.2 on 2020-03-11 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0005_auto_20200310_1853'),
        ('Telemetry', '0037_auto_20200304_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tlmyvartype',
            name='frameType',
        ),
        migrations.AddField(
            model_name='frametype',
            name='satellite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='framesTypes', to='GroundSegment.Satellite'),
        ),
    ]

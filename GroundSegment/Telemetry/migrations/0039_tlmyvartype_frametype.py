# Generated by Django 2.2.2 on 2020-03-11 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0038_auto_20200311_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlmyvartype',
            name='frameType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tlmyVarTypes', to='Telemetry.FrameType'),
        ),
    ]

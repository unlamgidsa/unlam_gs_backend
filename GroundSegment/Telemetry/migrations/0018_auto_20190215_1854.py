# Generated by Django 2.0.7 on 2019-02-15 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0017_tlmyvarlevel_satellite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlmyvarlevel',
            name='satellite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tlmyVarLevels', to='GroundSegment.Satellite'),
        ),
    ]

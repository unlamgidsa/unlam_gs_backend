# Generated by Django 2.2.1 on 2019-06-06 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0027_auto_20190606_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlmyvar',
            name='tlmyRawData',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tlmyVars', to='Telemetry.TlmyRawData'),
        ),
        migrations.AlterField(
            model_name='tlmyvartype',
            name='maxValue',
            field=models.FloatField(blank=True, null=True, verbose_name='Maximo valor tolerable'),
        ),
        migrations.AlterField(
            model_name='tlmyvartype',
            name='minValue',
            field=models.FloatField(blank=True, null=True, verbose_name='Minimo valor tolerable'),
        ),
    ]
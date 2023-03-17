# Generated by Django 4.1.7 on 2023-03-10 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0059_tlmyvar_fullname'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlmyvartype',
            name='UnixTimeStamp',
            field=models.FloatField(null=True, verbose_name='variable timestamp'),
        ),
        migrations.AddField(
            model_name='tlmyvartype',
            name='calSValue',
            field=models.CharField(help_text='Valor como string de la variable de telemetria', max_length=128, null=True, verbose_name='Valor como string de la variable de telemetria'),
        ),
        migrations.AddField(
            model_name='tlmyvartype',
            name='lastUpdate',
            field=models.DateTimeField(null=True, verbose_name='Indica cuando se escribio la variable'),
        ),
        migrations.AddField(
            model_name='tlmyvartype',
            name='lastUpdateTlmyVarId',
            field=models.BigIntegerField(null=True, verbose_name='pk related tlmyvar'),
        ),
    ]
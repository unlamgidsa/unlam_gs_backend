# Generated by Django 2.0.7 on 2019-02-14 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0012_auto_20181120_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='TlmyVarLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', help_text='Codigo, tipicamente L1, L2, L3', max_length=24, verbose_name='Codigo, tipicamente L1, L2, L3')),
                ('classname', models.CharField(default='', help_text='Nombre de la clase asociada', max_length=24, verbose_name='Nombre de la clase asociada')),
                ('timeRange', models.IntegerField(default=0, verbose_name='Delta de tiempo en segundos que integra el nivel')),
                ('queryRange', models.IntegerField(default=0, verbose_name='Delta de tiempo (En horas?)a partir del cual aplica el nivel')),
            ],
        ),
        migrations.AlterField(
            model_name='tlmyvartype',
            name='limitMaxValue',
            field=models.FloatField(default=99999.9, verbose_name='Maximo'),
        ),
        migrations.AlterField(
            model_name='tlmyvartype',
            name='limitMinValue',
            field=models.FloatField(default=-99999.9, verbose_name='Minimo'),
        ),
        migrations.AlterField(
            model_name='tlmyvartype',
            name='maxValue',
            field=models.FloatField(default=99999.9, verbose_name='Maximo valor tolerable'),
        ),
        migrations.AlterField(
            model_name='tlmyvartype',
            name='minValue',
            field=models.FloatField(default=-99999.9, verbose_name='Minimo valor tolerable'),
        ),
    ]
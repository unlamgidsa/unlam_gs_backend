# Generated by Django 2.2.1 on 2019-06-13 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0028_auto_20190606_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredictionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='NoDef', max_length=24, verbose_name='Code')),
                ('description', models.CharField(default='NoDef', max_length=512, verbose_name='Description')),
                ('aClass', models.CharField(default='NoDef', max_length=24, verbose_name='Class Name (Library)')),
            ],
        ),
        migrations.CreateModel(
            name='TlmyPrediction',
            fields=[
                ('tlmyVarType', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Telemetry.TlmyVarType')),
                ('updated', models.DateTimeField()),
                ('expiration', models.DateTimeField()),
                ('data', models.BinaryField()),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Telemetry.PredictionType')),
            ],
        ),
    ]
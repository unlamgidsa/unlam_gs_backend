# Generated by Django 4.0.6 on 2023-02-16 21:22

from django.db import migrations, models

def fullname_update(apps, schema_editor):
    tvts = apps.get_model('Telemetry', 'TlmyVarType').objects.all()
    for tv in tvts:
        tv.fullName = ''.join([tv.satellite.code,'.',tv.code])
        tv.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Telemetry', '0057_tlmyvar_rawvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlmyvartype',
            name='fullName',
            field=models.CharField(default='', help_text='fullname', max_length=64, verbose_name='fullname'),
        ),
        migrations.RunPython(fullname_update),
    ]
# Generated by Django 3.1.1 on 2020-09-08 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0008_auto_20200804_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useritem',
            name='jsonf',
            field=models.TextField(default=''),
        ),
    ]
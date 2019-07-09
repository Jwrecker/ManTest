# Generated by Django 2.2.3 on 2019-07-09 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowapp', '0005_auto_20190709_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steptype',
            name='step_type',
            field=models.CharField(choices=[('Load', 'Load URL'), ('Click', 'Click On'), ('Enter', 'Enter In'), ('Set', 'Set'), ('Verify', 'Verification')], max_length=15),
        ),
    ]

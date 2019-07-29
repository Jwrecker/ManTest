# Generated by Django 2.2.3 on 2019-07-29 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='step',
            old_name='fixture_name',
            new_name='fixture',
        ),
        migrations.RemoveField(
            model_name='step',
            name='has_fixture',
        ),
        migrations.RemoveField(
            model_name='step',
            name='item',
        ),
        migrations.AddField(
            model_name='step',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]

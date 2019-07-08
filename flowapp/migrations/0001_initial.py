# Generated by Django 2.2.3 on 2019-07-08 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('passed', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowapp.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('more', models.CharField(blank=True, max_length=200, null=True)),
                ('desired_result', models.CharField(max_length=500)),
                ('passed', models.BooleanField(default=False)),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowapp.Flow')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowapp.ActionTypes')),
            ],
        ),
    ]
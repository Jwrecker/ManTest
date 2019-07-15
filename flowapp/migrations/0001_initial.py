# Generated by Django 2.2.3 on 2019-07-15 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StepType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15, null=True)),
                ('url_validation', models.CharField(choices=[('Disallowed', 'Disallowed'), ('Optional', 'Optional'), ('Required', 'Required')], default='Optional', max_length=15)),
                ('has_verification', models.CharField(choices=[('Disallowed', 'Disallowed'), ('Optional', 'Optional'), ('Required', 'Required')], default='Optional', max_length=15)),
                ('has_fixture', models.CharField(choices=[('Disallowed', 'Disallowed'), ('Optional', 'Optional'), ('Required', 'Required')], default='Optional', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('passed', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=1)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowapp.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('desired_result', models.CharField(blank=True, max_length=500, null=True)),
                ('passed', models.BooleanField(blank=True, default=False, null=True)),
                ('has_fixture', models.BooleanField(default=False)),
                ('fixture_name', models.CharField(blank=True, max_length=100, null=True)),
                ('item', models.CharField(blank=True, max_length=100, null=True)),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowapp.Flow')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flowapp.StepType')),
            ],
            options={
                'ordering': ['order'],
                'index_together': {('flow', 'order')},
            },
        ),
    ]

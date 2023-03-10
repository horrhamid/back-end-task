# Generated by Django 4.1 on 2022-12-24 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_alter_apps_envs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apps',
            name='envs',
        ),
        migrations.CreateModel(
            name='Dicty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=250)),
                ('value', models.CharField(max_length=250)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='envs', to='apps.apps')),
            ],
        ),
    ]

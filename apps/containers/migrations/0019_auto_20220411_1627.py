# Generated by Django 3.2.12 on 2022-04-11 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0018_container_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='container_id',
        ),
        migrations.RemoveField(
            model_name='container',
            name='slug',
        ),
    ]
# Generated by Django 3.2.12 on 2022-02-22 19:06

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('containers', '0006_auto_20220222_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='start_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]

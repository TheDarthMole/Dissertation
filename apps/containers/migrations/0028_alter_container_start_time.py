# Generated by Django 4.0.4 on 2022-05-21 17:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0027_alter_container_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='start_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
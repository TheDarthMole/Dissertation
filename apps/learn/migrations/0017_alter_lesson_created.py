# Generated by Django 4.0.4 on 2022-05-21 17:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0016_remove_file_owner_remove_image_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

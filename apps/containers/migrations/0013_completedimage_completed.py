# Generated by Django 3.2.12 on 2022-03-14 12:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('containers', '0012_rename_completedimages_completedimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedimage',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]

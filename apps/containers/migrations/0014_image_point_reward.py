# Generated by Django 3.2.12 on 2022-03-15 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0013_completedimage_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='point_reward',
            field=models.IntegerField(default=0),
        ),
    ]

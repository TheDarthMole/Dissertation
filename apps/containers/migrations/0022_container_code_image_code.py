# Generated by Django 4.0.4 on 2022-04-14 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0021_auto_20220411_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='code',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='code',
            field=models.TextField(blank=True, null=True),
        ),
    ]
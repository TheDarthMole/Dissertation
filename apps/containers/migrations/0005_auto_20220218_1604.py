# Generated by Django 3.2.12 on 2022-02-18 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('containers', '0004_auto_20220218_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='image',
            name='tag',
            field=models.CharField(default='latest', max_length=16, null=True),
        ),
    ]

# Generated by Django 3.2.12 on 2022-02-16 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0002_alter_container_container_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='container_id',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
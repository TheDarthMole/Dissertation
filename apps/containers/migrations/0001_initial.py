# Generated by Django 3.2.12 on 2022-02-16 18:35

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_id', models.CharField(max_length=30)),
                ('container_name', models.CharField(max_length=30)),
                ('container_image', models.CharField(max_length=30)),
                ('container_id', models.CharField(max_length=12)),
                ('duration', models.IntegerField()),
                ('exposed_ports', models.CharField(max_length=150)),
                ('interactive_flag', models.BooleanField(default=False)),
                ('tty_flag', models.BooleanField(default=False)),
                ('rm_flag', models.BooleanField(default=True)),
            ],
        ),
    ]

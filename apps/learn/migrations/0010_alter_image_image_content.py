# Generated by Django 3.2.12 on 2022-03-08 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0009_alter_image_image_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_content',
            field=models.ImageField(upload_to='apps/static/images/lessons'),
        ),
    ]
# Generated by Django 5.0.6 on 2024-08-27 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0010_rename_image_imagemodel_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ImageModel',
        ),
    ]

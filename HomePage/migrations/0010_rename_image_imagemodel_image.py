# Generated by Django 5.0.6 on 2024-08-27 01:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0009_imagemodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagemodel',
            old_name='Image',
            new_name='image',
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-04 18:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0006_alter_graphmodel_graph'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphmodel',
            name='graph',
            field=models.FileField(upload_to='text/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt'])]),
        ),
    ]

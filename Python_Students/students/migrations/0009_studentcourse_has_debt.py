# Generated by Django 5.0.6 on 2024-05-22 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_debt'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourse',
            name='has_debt',
            field=models.BooleanField(default=False),
        ),
    ]

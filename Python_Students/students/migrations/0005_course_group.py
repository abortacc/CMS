# Generated by Django 5.0.6 on 2024-05-20 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_course_studentcourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='students.group'),
        ),
    ]

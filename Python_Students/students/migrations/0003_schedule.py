# Generated by Django 5.0.6 on 2024-05-20 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=256)),
                ('time', models.TimeField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.subject')),
            ],
        ),
    ]

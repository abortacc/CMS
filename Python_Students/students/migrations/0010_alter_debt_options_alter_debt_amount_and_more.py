# Generated by Django 5.0.6 on 2024-05-22 21:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_studentcourse_has_debt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='debt',
            options={},
        ),
        migrations.AlterField(
            model_name='debt',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='debt',
            name='count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='debt',
            name='debt_type',
            field=models.CharField(choices=[('financial', 'Financial'), ('academic', 'Academic')], max_length=10),
        ),
        migrations.AlterField(
            model_name='debt',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='debt',
            name='student_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.studentcourse'),
        ),
    ]

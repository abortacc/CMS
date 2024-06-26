# Generated by Django 5.0.6 on 2024-05-22 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_studentcourse_attended_hours'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Description')),
                ('debt_type', models.CharField(choices=[('financial', 'Financial'), ('academic', 'Academic')], max_length=10, verbose_name='Debt Type')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Amount')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='Count')),
                ('student_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.studentcourse', verbose_name='Student Course')),
            ],
            options={
                'verbose_name': 'Debt',
                'verbose_name_plural': 'Debts',
            },
        ),
    ]

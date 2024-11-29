# Generated by Django 5.1.3 on 2024-11-17 11:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0002_workouts_workout_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutexercise',
            name='repetitions',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)]),
        ),
    ]

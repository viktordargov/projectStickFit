from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from projectStickFit.workouts.choices import WorkoutTypeChoices

UserModel = get_user_model()


class Exercises(models.Model):
    exercise_name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        max_length=500,
    )

    def __str__(self):
        return self.exercise_name


class Workouts(models.Model):
    workout_name = models.CharField(
        max_length=200,
    )
    workout_description = models.TextField(
        max_length=500,
    )

    workout_type = models.CharField(
        choices=WorkoutTypeChoices.choices,
        default=WorkoutTypeChoices.TOTAL_BODY
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.workout_name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workouts,
        related_name='workout_exercises',
        on_delete=models.CASCADE,
    )

    exercise = models.ForeignKey(
        Exercises,
        on_delete=models.CASCADE,
    )

    order = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99),
        ],
        null=True,
        blank=True,
    )
    duration = models.DurationField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise.exercise_name} - {self.order}"


class WorkoutHistory(models.Model):
    workout = models.ForeignKey(
        to=Workouts,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    workout_date = models.DateField(
        auto_now_add=True,
    )

    workout_comments = models.TextField(
        null=True,
        blank=True,
    )

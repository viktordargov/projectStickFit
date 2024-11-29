from django.core.exceptions import ValidationError

from projectStickFit.workouts.models import WorkoutExercise


def validate_unique_order(workout, order):
    # Check if the order already exists in the current workout's exercises
    if WorkoutExercise.objects.filter(workout=workout, order=order).exists():
        raise ValidationError(f"An exercise with order {order} already exists in this workout.")
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectStickFit.settings')
django.setup()

from projectStickFit.workouts.models import Workouts, WorkoutExercise


def populate():
    workouts = [
        {"workout_name": "Total Body 1",
         "workout_description": "Total Body workout",
         "workout_type": "Total Body"},
        {"workout_name": "Dynamic balance 1",
         "workout_description": "Dynamic balance workout",
         "workout_type": "Dynamic Balance"},
        {"workout_name": "Muscle focus 1",
         "workout_description": "Muscle focus workout",
         "workout_type": "Muscle focus"},
    ]

    for workout in workouts:
        Workouts.objects.get_or_create(workout_name=workout["workout_name"],
                                       workout_description=workout["workout_description"])

    first_workout = Workouts.objects.get(workout_name="Dynamic balance 1",)

    workout_exercises = [
        {"order": 1,
         "repetitions": None,
         "duration": "0 years 0 mons 0 days 0 hours 0 mins 50.0 secs",
         "exercise_id": 52,
         "workout_id": first_workout.id
         },
        {"order": 2,
         "repetitions": 55,
         "duration": None,
         "exercise_id": 19,
         "workout_id": first_workout.id
         },
        {"order": 3,
         "repetitions": None,
         "duration": "0 years 0 mons 0 days 0 hours 0 mins 30.0 secs",
         "exercise_id": 58,
         "workout_id": first_workout.id
         },
    ]

    for workout_exercise in workout_exercises:
        WorkoutExercise.objects.get_or_create(order=workout_exercise["order"], duration=workout_exercise["duration"],
                                              repetitions=workout_exercise["repetitions"],
                                              exercise_id=workout_exercise["exercise_id"],
                                              workout_id=workout_exercise["workout_id"])


if __name__ == '__main__':
    populate()

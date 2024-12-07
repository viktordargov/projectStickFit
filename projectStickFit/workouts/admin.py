from django.contrib import admin

from projectStickFit.workouts.forms import WorkoutAdd, AddExercise, WorkoutExerciseForm
from projectStickFit.workouts.models import Workouts, Exercises, WorkoutExercise


@admin.register(Workouts)
class WorkoutsAdmin(admin.ModelAdmin):
    model = Workouts
    add_form = WorkoutAdd

    list_display = ('pk', 'workout_name', 'workout_type', 'short_description', 'created_at',)
    search_fields = ('workout_name', 'workout_type', 'short_description',)
    ordering = ('created_at',)

    fieldsets = (
        (None, {'fields': ('workout_name', 'workout_description')}),
    )

    def short_description(self, obj):
        return obj.workout_description[:50] + '...' if len(obj.workout_description) > 50 else obj.workout_description

    short_description.short_description = 'workout_description'


@admin.register(Exercises)
class ExercisesAdmin(admin.ModelAdmin):
    model = Exercises
    add_form = AddExercise

    list_display = ('pk', 'exercise_name',)
    search_fields = ('exercise_name',)
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': ('exercise_name', 'description')}),
    )


@admin.register(WorkoutExercise)
class ExercisesAdmin(admin.ModelAdmin):
    model = WorkoutExercise
    add_form = WorkoutExerciseForm

    list_display = (
        'pk', 'order', 'workout__workout_name', 'workout__workout_type', 'exercise__exercise_name', 'repetitions', 'duration',)
    search_fields = ('workout__workout_name', 'workout__workout_type', 'exercise__exercise_name',)
    ordering = ('order',)

from django import forms
from django.db.models import Max
from .models import Workouts, Exercises, WorkoutHistory, WorkoutExercise
from .validators import validate_unique_order


class WorkoutsBaseForm(forms.ModelForm):
    class Meta:
        model = Workouts
        fields = '__all__'


class WorkoutAdd(WorkoutsBaseForm):
    pass


class WorkoutUpdate(WorkoutsBaseForm):
    pass


class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'order', 'repetitions', 'duration']
        widgets = {
            'exercise': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        # Accept workout parameter and store it on the instance
        self.workout = kwargs.pop('workout', None)
        super().__init__(*args, **kwargs)
        max_order = WorkoutExercise.objects.filter(workout=self.workout).aggregate(Max('order'))['order__max']
        self.fields['order'].initial = (max_order + 1) if max_order else 1

    def clean(self):
        cleaned_data = super().clean()
        order = cleaned_data.get('order')

        # If we have a workout associated with the instance, validate the order
        if self.workout:
            validate_unique_order(self.workout, order)

        return cleaned_data


class ExerciseBaseForm(forms.ModelForm):
    class Meta:
        model = Exercises
        fields = '__all__'


class AddExercise(ExerciseBaseForm):
    pass


class EditExercise(ExerciseBaseForm):
    pass


class WorkoutHistoryForm(forms.ModelForm):
    class Meta:
        model = WorkoutHistory
        fields = ['workout_comments']

        widgets = {
            'workout_comments': forms.Textarea(attrs={'placeholder': 'How did you do this time?'}),
        }

        labels = {
            'workout_comments': 'Workout remarks',
        }

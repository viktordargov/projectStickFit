import json
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, TemplateView, DeleteView
from projectStickFit.common.mixins import IsStaffMixin
from projectStickFit.workouts.forms import WorkoutAdd, AddExercise, WorkoutHistoryForm, WorkoutExerciseForm
from projectStickFit.workouts.models import Workouts, Exercises, WorkoutHistory, WorkoutExercise


# Create your views here.

class WorkoutsListView(ListView):
    model = Workouts
    template_name = 'workouts/workouts-list.html'
    context_object_name = 'workouts'

    def get_queryset(self):
        queryset = Workouts.objects.all()
        user_query = self.request.GET.get('user_query', '')

        if user_query:
            # Filter by specific columns
            return queryset.filter(
                Q(workout_name__icontains=user_query) | Q(workout_description__icontains=user_query) | Q(
                    workout_type__icontains=user_query),
            )
        return Workouts.objects.all()


class WorkoutsCreateView(LoginRequiredMixin, IsStaffMixin, CreateView):
    model = Workouts
    form_class = WorkoutAdd
    template_name = 'workouts/workout-add.html'
    success_url = reverse_lazy('edit_workout')

    def form_valid(self, form):
        # Customizing the form_valid method to ensure redirection to the edit page with the workout ID
        workout = form.save()
        return redirect('edit_workout', workout_id=workout.id)


class WorkoutEditView(TemplateView):
    template_name = 'workouts/workout-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout_id = kwargs['workout_id']
        workout = get_object_or_404(Workouts, id=workout_id)
        exercises = Exercises.objects.all()  # All available exercises
        workout_exercises = workout.workout_exercises.all()  # Exercises already added to the workout

        form = WorkoutExerciseForm(workout=workout)

        context.update({
            'workout': workout,
            'exercises': exercises,
            'workout_exercises': workout_exercises,
            'form': form,
        })
        return context

    def post(self, request, *args, **kwargs):
        workout_id = kwargs['workout_id']
        workout = get_object_or_404(Workouts, id=workout_id)
        form = WorkoutExerciseForm(request.POST, workout=workout)
        if form.is_valid():
            # Save the workout exercise to the workout
            workout_exercise = form.save(commit=False)
            workout_exercise.workout = workout
            workout_exercise.save()
            return redirect('edit_workout', workout_id=workout.id)
        context = self.get_context_data(workout_id=workout_id)  # Pass workout_id explicitly
        context['form'] = form  # Ensure the invalid form is added to context
        return self.render_to_response(context)


class WorkoutsDetailView(LoginRequiredMixin, DetailView):
    model = Workouts
    template_name = 'workouts/workout-detail.html'
    context_object_name = 'workouts'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        workout = self.get_object()
        exercises = workout.workout_exercises.all()

        context['workout_history'] = WorkoutHistoryForm()
        context['exercises'] = exercises
        exercises_list = []
        for exercise in exercises:
            # Convert the `timedelta` to seconds if it exists
            duration_seconds = int(exercise.duration.total_seconds()) if exercise.duration else None
            exercises_list.append({
                'name': exercise.exercise.exercise_name,
                'duration': duration_seconds,
                'repetition': exercise.repetitions
            })

        # Pass the exercises as a JSON string to the template
        context['exercises_json'] = json.dumps(exercises_list)

        return context

    def post(self, request, *args, **kwargs):
        workout = get_object_or_404(Workouts, id=self.kwargs['pk'])  # Get the current training object
        form = WorkoutHistoryForm(request.POST)

        if form.is_valid():
            # Save the form with the user and training automatically filled
            training_session = form.save(commit=False)
            training_session.user = request.user  # Associate the logged-in user
            training_session.workout = workout  # Associate the current training
            training_session.save()  # Save to database

            return redirect('home')


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workouts
    success_url = reverse_lazy('workouts_list')

    def get(self, request, *args, **kwargs):
        workout = get_object_or_404(Workouts, id=self.kwargs['pk'])
        workout.delete()
        return redirect(self.success_url)


class WorkoutExerciseDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutExercise

    def get(self, request, *args, **kwargs):
        workout_exercise = get_object_or_404(WorkoutExercise, id=self.kwargs['pk'])
        workout_exercise.delete()
        return redirect('edit_workout', workout_id=workout_exercise.workout_id)


class WorkoutHistoryListView(LoginRequiredMixin, ListView):
    model = WorkoutHistory
    template_name = 'workouts/workout-history.html'
    context_object_name = 'workout_history'

    def get_queryset(self):
        return WorkoutHistory.objects.filter(user=self.request.user)


class WorkoutHistoryDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutHistory

    def post(self, request, *args, **kwargs):
        user = request.user
        WorkoutHistory.objects.filter(user=user).delete()
        return redirect('workout_history')


class ExerciseListView(ListView):
    model = Exercises
    template_name = 'workouts/exercise-list.html'
    context_object_name = 'exercises'


class ExerciseCreateView(CreateView):
    model = Exercises
    form_class = AddExercise
    template_name = 'workouts/exercise-add.html'
    success_url = reverse_lazy('exercise_list')


class ExerciseDeleteView(LoginRequiredMixin, DeleteView):
    model = Exercises
    success_url = reverse_lazy('exercise_list')

    def get(self, request, *args, **kwargs):
        exercise = get_object_or_404(Exercises, id=self.kwargs['pk'])
        exercise.delete()
        return redirect(self.success_url)

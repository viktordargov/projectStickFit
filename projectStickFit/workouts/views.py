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
    ordering = ['-created_at']
    paginate_by = 15

    def get_queryset(self):
        queryset = Workouts.objects.all()
        user_query = self.request.GET.get('user_query', '')

        if user_query:
            # Filter by specific columns
            return queryset.filter(
                Q(workout_name__icontains=user_query) | Q(workout_description__icontains=user_query) | Q(
                    workout_type__icontains=user_query),
            ).order_by('-created_at')
        return Workouts.objects.all().order_by('-created_at')


class WorkoutsCreateView(LoginRequiredMixin, IsStaffMixin, CreateView):
    model = Workouts
    form_class = WorkoutAdd
    template_name = 'workouts/workout-add.html'
    success_url = reverse_lazy('edit_workout')

    def form_valid(self, form):
        workout = form.save()
        return redirect('edit_workout', workout_id=workout.id)


class WorkoutEditView(LoginRequiredMixin, IsStaffMixin, TemplateView):
    template_name = 'workouts/workout-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout_id = kwargs['workout_id']
        workout = get_object_or_404(Workouts, id=workout_id)
        exercises = Exercises.objects.all()
        workout_exercises = workout.workout_exercises.all()

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
            workout_exercise = form.save(commit=False)
            workout_exercise.workout = workout
            workout_exercise.save()
            return redirect('edit_workout', workout_id=workout.id)
        context = self.get_context_data(workout_id=workout_id)
        context['form'] = form
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
            duration_seconds = int(exercise.duration.total_seconds()) if exercise.duration else None
            exercises_list.append({
                'name': exercise.exercise.exercise_name,
                'duration': duration_seconds,
                'repetition': exercise.repetitions
            })

        context['exercises_json'] = json.dumps(exercises_list)

        return context

    def post(self, request, *args, **kwargs):
        workout = get_object_or_404(Workouts, id=self.kwargs['pk'])
        form = WorkoutHistoryForm(request.POST)

        if form.is_valid():

            training_session = form.save(commit=False)
            training_session.user = request.user
            training_session.workout = workout
            training_session.save()

            return redirect('home')


class WorkoutDeleteView(LoginRequiredMixin, IsStaffMixin, DeleteView):
    model = Workouts
    success_url = reverse_lazy('workouts_list')

    def get(self, request, *args, **kwargs):
        workout = get_object_or_404(Workouts, id=self.kwargs['pk'])
        workout.delete()
        return redirect(self.success_url)


class WorkoutExerciseDeleteView(LoginRequiredMixin, IsStaffMixin, DeleteView):
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


class ExerciseListView(LoginRequiredMixin, ListView):
    model = Exercises
    template_name = 'workouts/exercise-list.html'
    context_object_name = 'exercises'
    paginate_by = 15


class ExerciseCreateView(LoginRequiredMixin, IsStaffMixin, CreateView):
    model = Exercises
    form_class = AddExercise
    template_name = 'workouts/exercise-add.html'
    success_url = reverse_lazy('exercise_list')


class ExerciseDeleteView(LoginRequiredMixin, IsStaffMixin, DeleteView):
    model = Exercises
    success_url = reverse_lazy('exercise_list')

    def get(self, request, *args, **kwargs):
        exercise = get_object_or_404(Exercises, id=self.kwargs['pk'])
        exercise.delete()
        return redirect(self.success_url)

import random

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from projectStickFit.workouts.models import WorkoutHistory, Workouts


class HomePage(TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            recent_workouts = WorkoutHistory.objects.filter(user=self.request.user).order_by('-workout_date')[:5]
            workout_count = WorkoutHistory.objects.filter(user=self.request.user).count()
            # total_hours = sum([workout.duration for workout in WorkoutHistory.objects.filter(user=self.request.user)])
            context['recent_workouts'] = recent_workouts
            context['workout_count'] = workout_count
            context['total_hours'] = 0
        else:
            context['recent_workouts'] = []
            context['workout_count'] = 0
            context['total_hours'] = 0

        return context


@login_required
def random_workout(request):
    workouts = Workouts.objects.all()
    random_wt = random.choice(workouts)
    return redirect('workout_detail', pk=random_wt.pk)


def custom_404_view(request, exception):
    return render(request, "404.html", status=404)

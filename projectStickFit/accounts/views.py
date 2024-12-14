from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from projectStickFit.accounts.forms import AppUserCreationForm, ProfileEditForm
from projectStickFit.accounts.models import AppProfile
from projectStickFit.workouts.models import WorkoutHistory

from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect

UserModel = get_user_model()


class AppUserLogin(LoginView):
    template_name = 'accounts/login-page.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)


class AppUserRegistrationView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response


class AppUserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = AppProfile.objects.get(user=self.request.user)

        recent_workouts = WorkoutHistory.objects.filter(user=self.request.user).order_by('-workout_date')[:15]
        workout_count = WorkoutHistory.objects.filter(user=self.request.user).count()
        # total_hours = sum([workout.duration for workout in WorkoutHistory.objects.filter(user=self.request.user)])

        context['recent_workouts'] = recent_workouts
        context['workout_count'] = workout_count
        context['total_hours'] = 0

        return context


class AppUserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = AppProfile
    form_class = ProfileEditForm
    context_object_name = 'profile'
    template_name = 'accounts/profile-edit.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if not self.request.user.is_staff and obj.user != self.request.user:
            return None

        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj is None:
            return redirect('profile_edit', pk=request.user.profile.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'profile',
            kwargs={'pk': self.object.pk},
        )


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                token_generator=default_token_generator,
            )
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'accounts/password_reset_form.html', {'form': form})


def logout_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    return LogoutView.as_view()(request, *args, **kwargs)

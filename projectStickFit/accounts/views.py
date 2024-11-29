from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView

from projectStickFit.accounts.forms import AppUserCreationForm, ProfileEditForm
from projectStickFit.accounts.models import AppProfile

UserModel = get_user_model()


# Create your views here.

class AppUserLogin(LoginView):
    template_name = 'accounts/login-page.html'


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
        return context


class AppUserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = AppProfile
    form_class = ProfileEditForm
    context_object_name = 'profile'
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy(
            'profile',
            kwargs={'pk': self.object.pk},
        )

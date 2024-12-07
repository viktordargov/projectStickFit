from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

from projectStickFit.accounts.models import AppProfile

UserModel = get_user_model()


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = AppProfile
        exclude = ('user',)

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

        labels = {
            'date_of_birth': 'Date of Birth',
            'weight': 'Weight (kg)',
            'height': 'Height (cm)',
        }



from django.contrib.auth.views import LogoutView
from django.urls import path, include

from projectStickFit.accounts import views

urlpatterns = [
    path('login/', views.AppUserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.AppUserRegistrationView.as_view(), name='register'),

    path('profile/<int:pk>/', include([
        path('', views.AppUserProfileView.as_view(), name='profile'),
        path('edit/', views.AppUserProfileUpdateView.as_view(), name='profile_edit'),
    ])),
]

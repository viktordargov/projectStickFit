from django.contrib.auth import views as auth_views
from django.urls import path, include

from projectStickFit.accounts import views

urlpatterns = [
    path('login/', views.AppUserLogin.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.AppUserRegistrationView.as_view(), name='register'),

    path('profile/<int:pk>/', include([
        path('', views.AppUserProfileView.as_view(), name='profile'),
        path('edit/', views.AppUserProfileUpdateView.as_view(), name='profile_edit'),
    ])),
    path('reset-request/', views.password_reset_request, name='password_reset_request'),

    # Built-in password reset views
    path('reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]

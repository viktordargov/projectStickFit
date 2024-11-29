from django.urls import path

from projectStickFit.common import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
]
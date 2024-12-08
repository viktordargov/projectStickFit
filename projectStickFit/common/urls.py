from django.urls import path
from django.conf.urls import handler404
from projectStickFit.common import views
from projectStickFit.common.views import random_workout

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('random-workout/', random_workout, name='random_workout'),
]


handler404 = views.custom_404_view
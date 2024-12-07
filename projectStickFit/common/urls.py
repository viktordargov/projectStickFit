from django.urls import path
from django.conf.urls import handler404
from projectStickFit.common import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
]


handler404 = views.custom_404_view
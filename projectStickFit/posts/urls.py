from django.urls import path

from projectStickFit.posts import views

urlpatterns = [
    path('', views.post_list, name='posts_list'),
    path('create_post/', views.create_post, name='create_post'),
]

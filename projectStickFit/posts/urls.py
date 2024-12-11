from django.urls import path

from projectStickFit.posts import views

urlpatterns = [
    path('', views.post_list, name='posts_list'),
    path('create_post/', views.create_post, name='create_post'),
    path('delete-image/', views.DeleteImageView.as_view(), name='delete_post'),
]

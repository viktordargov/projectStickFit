from django.urls import path

from projectStickFit.forum import views

urlpatterns = [
    path('', views.ForumPostListView.as_view(), name='forum_list'),
    path('post/<int:pk>/', views.ForumPostDetailView.as_view(), name='forum_post_detail'),
    path('create/', views.ForumPostCreateView.as_view(), name='create_forum_post'),
    path('like/<int:pk>/', views.LikePostView.as_view(), name='like_post'),
]
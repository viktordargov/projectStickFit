from django.urls import path

from projectStickFit.forum import views

urlpatterns = [
    path('', views.ForumThreadListView.as_view(), name='forum_list'),
    path('thread/<int:pk>/', views.ForumThreadDetailView.as_view(), name='forum_thread_detail'),
    path('create/', views.ForumThreadCreateView.as_view(), name='create_forum_thread'),
    path('like/<int:pk>/', views.LikeThreadView.as_view(), name='like_thread'),
]
from django.urls import path, include

from projectStickFit.forum import views

urlpatterns = [
    path('', views.ForumThreadListView.as_view(), name='forum_list'),
    path('thread/<int:pk>/', include([
        path('', views.ForumThreadDetailView.as_view(), name='forum_thread_detail'),
        path('delete/', views.ForumThreadDeleteView.as_view(), name='delete_forum_thread'),
    ])),
    path('create/', views.ForumThreadCreateView.as_view(), name='create_forum_thread'),
    path('like/<int:pk>/', views.LikeThreadView.as_view(), name='like_thread'),
]

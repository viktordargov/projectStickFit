from django.urls import path, include

from projectStickFit.workouts import views

urlpatterns = [
    path('', views.WorkoutsListView.as_view(), name='workouts_list'),
    path('exercises/', views.ExerciseListView.as_view(), name='exercise_list'),
    path('add-workout/', views.WorkoutsCreateView.as_view(), name='add_workout'),
    path('add-exercise/', views.ExerciseCreateView.as_view(), name='add_exercise'),
    path('history/', views.WorkoutHistoryListView.as_view(), name='workout_history'),
    path('workout/<int:pk>/', include([
        path('', views.WorkoutsDetailView.as_view(), name='workout_detail'),
        path('delete/', views.WorkoutDeleteView.as_view(), name='workout_delete'),
    ])),
    path('exercise/<int:pk>/', include([
        path('delete/', views.ExerciseDeleteView.as_view(), name='exercise_delete'),
    ])),
    path('edit-workout/<int:workout_id>/', views.WorkoutEditView.as_view(), name='edit_workout'),

    path('workout-exercise-delete/<int:pk>', views.WorkoutExerciseDeleteView.as_view(),
         name='workout_exercise_delete'),

]

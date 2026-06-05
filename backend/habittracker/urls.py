from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list_view, name='habit_list'),
    path('create/', views.habit_create_view, name='habit_create'),
    path('<int:pk>/edit/', views.habit_edit_view, name='habit_edit'),
    path('<int:pk>/delete/', views.habit_delete_view, name='habit_delete'),
    path('<int:pk>/log/', views.habit_log_view, name='habit_log'),
    path('<int:pk>/heatmap/', views.habit_heatmap_view, name='habit_heatmap'),
]
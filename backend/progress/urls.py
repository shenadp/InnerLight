from django.urls import path
from . import views

urlpatterns = [
    path('', views.progress_view, name='progress'),
    path('weekly/', views.weekly_report_view, name='weekly_report'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('achievements/<int:pk>/share/', views.share_achievement_view, name='share_achievement'),
]
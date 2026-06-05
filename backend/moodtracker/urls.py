from django.urls import path
from . import views

urlpatterns = [
    path('checkin/', views.mood_checkin_view, name='mood_checkin'),
    path('insights/', views.mood_insights_view, name='mood_insights'),
    path('history/', views.mood_history_view, name='mood_history'),
]
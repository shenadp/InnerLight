from django.urls import path
from . import views

urlpatterns = [
    path('breathing/', views.breathing_view, name='breathing'),
    path('ambient/', views.ambient_view, name='ambient'),
    path('affirmation/', views.affirmation_view, name='affirmation'),
    path('', views.calm_view, name='calm_home'),
]
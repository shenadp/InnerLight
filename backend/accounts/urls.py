from django.urls import path
from . import views
from .views import set_theme_view

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('set-theme/', set_theme_view, name='set_theme'),
]
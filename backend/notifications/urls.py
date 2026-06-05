from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_settings_view, name='notification_settings'),
    path('create/', views.notification_create_view, name='notification_create'),
    path('<int:pk>/delete/', views.notification_delete_view, name='notification_delete'),
    path('log/', views.notification_log_view, name='notification_log'),
]
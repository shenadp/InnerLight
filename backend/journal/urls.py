from django.urls import path
from . import views

urlpatterns = [
    path('', views.journal_list_view, name='journal_list'),
    path('create/', views.journal_create_view, name='journal_create'),
    path('<int:pk>/', views.journal_detail_view, name='journal_detail'),
    path('<int:pk>/edit/', views.journal_edit_view, name='journal_edit'),
    path('<int:pk>/delete/', views.journal_delete_view, name='journal_delete'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.igp_entry, name='igp_entry'),
    path('processed_igp_creation/', views.process_create_igp, name='process_create_igp'),
    path('view/', views.view_igp, name='view_igp'),
    path('update/<int:pk>/', views.update_igp, name='update_igp'),
    path('delete/<int:pk>/', views.delete_igp, name='delete_igp'),
]

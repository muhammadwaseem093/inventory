from django.urls import path 
from . import views

urlpatterns = [
    path('create/', views.create_type, name='create_type'),
    path('processed_type_creation', views.process_type_creation, name='process_type_creation'),
    path('list/', views.type_list, name='type_list'),
    path('edit/<int:type_id>/', views.edit_type, name='edit_type'),
    path('processed_type_update/<int:type_id>/', views.process_type_update, name='process_type_update'),
    path('delete/<int:type_id>/', views.delete_type, name='delete_type'),
]
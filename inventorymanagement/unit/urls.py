from django.urls import path 
from . import views

urlpatterns = [
    path('create/', views.create_unit, name='create_unit'),
    path('process_unit_creation/', views.process_unit_creation, name='process_unit_creation'),
    path('list/', views.unit_list, name='unit_list'),
    path('edit/<int:unit_id>/', views.edit_unit, name='edit_unit'),
    path('process_unit_edit/<int:unit_id>/', views.process_unit_edit, name='process_unit_edit'),
    path('delete/<int:unit_id>/', views.delete_unit, name='delete_unit'),
]
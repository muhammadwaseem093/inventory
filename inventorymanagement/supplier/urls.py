from django.urls import path 
from . import views

urlpatterns = [
    path('create/', views.create_supplier, name='create_supplier'),
    path('process_supplier_creation/', views.process_supplier_creation, name='process_supplier_creation'),
    path('list/', views.supplier_list, name='supplier_list'),
    path('edit/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('process_supplier_edit/<int:supplier_id>/', views.process_supplier_edit, name='process_supplier_edit'),
    path('delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
]
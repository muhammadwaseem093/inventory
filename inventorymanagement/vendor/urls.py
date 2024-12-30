from django.urls import path 
from . import views

urlpatterns = [
    path('create/', views.create_vendor, name='create_vendor'),
    path('process_vendor_creation/', views.process_vendor_creation, name='process_vendor_creation'),
    path('list/', views.vendor_list, name='vendor_list'),
    path('edit/<int:vendor_id>/', views.edit_vendor, name='edit_vendor'),
    path('process_vendor_edit/<int:vendor_id>/', views.process_vendor_edit, name='process_vendor_edit'),
    path('delete/<int:vendor_id>/', views.delete_vendor, name='delete_vendor'),
]
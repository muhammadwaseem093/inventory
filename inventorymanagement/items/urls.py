from django.urls import path 
from . import views

urlpatterns = [
    path('create/', views.create_item, name='create_item'),
    path('process_item_creation/', views.process_item_creation, name='process_item_creation'),
    path('list/', views.item_list, name='item_list'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('process_item_edit/<int:item_id>/', views.process_item_edit, name='process_item_edit'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]
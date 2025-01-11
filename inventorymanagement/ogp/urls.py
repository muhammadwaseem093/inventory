from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.ogp_entry, name='ogp_entry'),
    path('processed_ogp_creation/', views.process_create_ogp, name='process_create_ogp'),
    path('add-item/', views.process_ogp_item, name='process_ogp_item'),
    path('view/', views.view_ogp, name='view_ogp'),
    path('update/<int:pk>/', views.update_ogp, name='update_ogp'),
    path('delete/<int:pk>/', views.delete_ogp, name='delete_ogp'),
    path('get-filtered-data/', views.get_filtered_data, name='get_filtered_data'),
]

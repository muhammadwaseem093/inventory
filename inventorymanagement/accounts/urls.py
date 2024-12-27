# accounts/urls.py
from django.urls import path
from .views import super_admin_dashboard, admin_dashboard, staff_dashboard, login_view,logout_view,register_view

urlpatterns = [
    path('super-admin/', super_admin_dashboard, name='super_admin_dashboard'),
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('staff/', staff_dashboard, name='staff_dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]

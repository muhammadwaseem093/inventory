# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    STAFF = 'staff'
    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
    ]
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, default=STAFF)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
    
class ActivityLog(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    activity_name=models.CharField(max_length=255)
    activity_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_name}"

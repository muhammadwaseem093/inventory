from django.db import models

# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
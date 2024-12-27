from django.db import models
from django.utils import timezone

class IGP(models.Model):
    igp_number = models.CharField(max_length=20, unique=True)
    messer = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    vehicle_type = models.CharField(
        max_length=20,
        choices=[
            ('mazda', 'Mazda'),
            ('toyota', 'Toyota'),
            ('suzuki', 'Suzuki'),
        ],
        default='mazda'
    )
    driver_name = models.CharField(max_length=50, blank=True, null=True)
    driver_cnic = models.CharField(max_length=15, blank=True, null=True)
    type = models.CharField(
        max_length=50,
        choices=[
            ('Raw Material', 'Raw Material'),
            ('Inward', 'Inward'),
        ],
        default='Inward'
    )
    address = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"IGP {self.igp_number} - {self.messer}"


class Item(models.Model):
    igp = models.ManyToManyField(IGP, related_name='items')
    sr_no = models.PositiveIntegerField()
    description = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Item {self.sr_no} for IGP {self.igp.igp_number}"

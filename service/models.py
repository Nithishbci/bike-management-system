from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import datetime

class RiderProfile(AbstractUser):
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    rider_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class MechanicDetails(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class ServiceBookingRecord(models.Model):
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bike_model = models.CharField(max_length=100)
    service_date = models.DateField(default=datetime.now)
    preferred_time = models.TimeField(default=datetime.now)
    mechanic_assigned = models.ForeignKey(MechanicDetails, on_delete=models.SET_NULL, null=True, blank=True)
    service_status = models.CharField(max_length=50, default='Pending')  # Pending, In Progress, Completed

    def __str__(self):
        return f"Service for {self.bike_model} on {self.service_date} by {self.booked_by}"
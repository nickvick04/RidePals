from django.db import models

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    origination_city = models.CharField(max_length=100, default='')
    origination_state = models.CharField(max_length=2, default='')
    destination_city = models.CharField(max_length=100)
    destination_state = models.CharField(max_length=2)
    date = models.DateField()
    time = models.TimeField()
    taking_passengers = models.BooleanField()
    seats_available = models.IntegerField()
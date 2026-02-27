from django.db import models

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    origination_city = models.CharField(max_length=100, default='')
    origination_state = models.CharField(max_length=2, default='')
    destination_city = models.CharField(max_length=100)
    destination_state = models.CharField(max_length=2)
    date = models.DateField()
    time = models.TimeField()
    taking_passengers = models.BooleanField()
    seats_available = models.IntegerField()
    vehicle_type = models.CharField(max_length=100, blank=True)
    car_class = models.CharField(
        max_length=20,
        choices=[("regular", "Regular"), ("premium", "Premium")],
        default="regular",
    )


class Booking(models.Model):
    ride = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="bookings")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)
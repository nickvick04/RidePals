from django import forms

from .models import Person


class RideForm(forms.Form):
  origin = forms.CharField(
    label='Leaving From', 
    max_length=100,
    required=False,
    widget=forms.TextInput(attrs={
      'placeholder': 'e.g., San Fransisco, CA',
      'class': 'form-control'
    })
  )
  
  destination = forms.CharField(
    label='Heading To', 
    max_length=100,
    required=False,
    widget=forms.TextInput(attrs={
      'placeholder': 'e.g., Los Angeles, CA',
      'class': 'form-control'
    })
  )


class NewRideForm(forms.ModelForm):
  class Meta:
    model = Person
    fields = [
      "first_name",
      "last_name",
      "email",
      "origination_city",
      "origination_state",
      "destination_city",
      "destination_state",
      "date",
      "time",
      "taking_passengers",
      "seats_available",
      "vehicle_type",
    ]
    widgets = {
      "date": forms.DateInput(attrs={"type": "date"}),
      "time": forms.TimeInput(attrs={"type": "time"}),
    }

  def save(self, commit=True):
    """
    Automatically classify car_class based on vehicle_type.
    Defaults to 'regular' unless vehicle is a premium brand.
    """
    instance = super().save(commit=False)

    premium_brands = [
      "rolls-royce",
      "bentley",
      "bugatti",
      "maybach",
      "mercedes-benz",
      "mercedes",
      "bmw",
      "audi",
      "lexus",
      "porsche",
    ]

    vehicle = (instance.vehicle_type or "").lower()
    if any(brand in vehicle for brand in premium_brands):
      instance.car_class = "premium"
    else:
      instance.car_class = "regular"

    if commit:
      instance.save()
    return instance


class BookingForm(forms.Form):
  first_name = forms.CharField(max_length=100, label="Your first name")
  last_name = forms.CharField(max_length=100, label="Your last name")
  email = forms.EmailField(label="Your email")
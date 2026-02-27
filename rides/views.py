from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from datetime import date, datetime

from .models import Person, Booking

# relative import of forms
from .forms import RideForm, NewRideForm, BookingForm

# Create your views here.


def parse_location(location_string):
  """
  Parse a location string like "Los Angeles, CA" or "Los Angeles CA"
  Returns a tuple of (city, state) or (None, None) if invalid
  """
  if not location_string:
    return None, None
  
  # Remove extra whitespace
  location_string = location_string.strip()
  
  # Try splitting by comma first
  if ',' in location_string:
    parts = location_string.split(',')
    if len(parts) == 2:
      city = parts[0].strip()
      state = parts[1].strip().upper()
      return city, state
  
  # If no comma, split by space and check if last part looks like a state (2 chars)
  parts = location_string.rsplit(None, 1)  # Split from right, max 1 split
  if len(parts) == 2:
    potential_state = parts[1].strip()
    # Only treat as state if it's exactly 2 characters (state abbreviation)
    if len(potential_state) == 2 and potential_state.isalpha():
      city = parts[0].strip()
      state = potential_state.upper()
      return city, state
    else:
      # The "state" part is actually part of the city name
      return location_string, None
  elif len(parts) == 1:
    # Only one part, could be just city or just state
    part = parts[0].strip()
    if len(part) == 2 and part.isalpha():
      # Likely a state abbreviation
      return None, part.upper()
    else:
      # Likely a city name
      return part, None
  
  return None, None


def search(request):
  print("HIT SEARCH VIEW")
  context = {}

  # Start with future rides only (hide past trips)
  today = date.today()
  now_time = datetime.now().time()

  people = Person.objects.filter(
    Q(date__gt=today) | Q(date=today, time__gte=now_time)
  )

  if "origin" in request.GET or "destination" in request.GET:
    context["inputExists"] = True
    
    origin_input = request.GET.get("origin", "").strip()
    destination_input = request.GET.get("destination", "").strip()
    
    # Parse the inputs
    origin_city, origin_state = parse_location(origin_input)
    destination_city, destination_state = parse_location(destination_input)
    
    # Filter by origin if provided
    if origin_city or origin_state:
      origin_filter = Q()
      if origin_city:
        origin_filter &= Q(origination_city__iexact=origin_city)
      if origin_state:
        origin_filter &= Q(origination_state__iexact=origin_state)
      people = people.filter(origin_filter)
    
    # Filter by destination if provided
    if destination_city or destination_state:
      destination_filter = Q()
      if destination_city:
        destination_filter &= Q(destination_city__iexact=destination_city)
      if destination_state:
        destination_filter &= Q(destination_state__iexact=destination_state)
      people = people.filter(destination_filter)

  context["people"] = people
  context["form"] = RideForm()

  return render(request, "index_view.html", context)


def ride_detail(request, ride_id):
  """Show details for a single ride and its booking status."""
  ride = get_object_or_404(Person, id=ride_id)

  # Determine if this ride is in the past
  today = date.today()
  now_time = datetime.now().time()
  is_past = (ride.date < today) or (ride.date == today and ride.time < now_time)

  passengers = ride.bookings.order_by("booked_at")

  context = {
    "ride": ride,
    "is_past": is_past,
    "is_full": ride.seats_available <= 0,
    "passengers": passengers,
    "booking_form": BookingForm(),
  }
  return render(request, "ride_detail.html", context)


def book_seat(request, ride_id):
  """Book a single seat on a ride, if available and not in the past."""
  ride = get_object_or_404(Person, id=ride_id)

  today = date.today()
  now_time = datetime.now().time()
  is_past = (ride.date < today) or (ride.date == today and ride.time < now_time)

  if request.method != "POST":
    return redirect("rides:detail", ride_id=ride.id)

  form = BookingForm(request.POST)
  if not form.is_valid():
    messages.error(request, "Please correct the booking details below.")
    today = date.today()
    now_time = datetime.now().time()
    is_past = (ride.date < today) or (ride.date == today and ride.time < now_time)
    context = {
      "ride": ride,
      "is_past": is_past,
      "is_full": ride.seats_available <= 0,
      "booking_form": form,
    }
    return render(request, "ride_detail.html", context)

  if is_past:
    messages.error(request, "This ride has already departed and can no longer be booked.")
  elif ride.seats_available <= 0:
    messages.error(request, "This ride is full and has no seats left to book.")
  else:
    # At this point, booking details are valid; store them and update seats.
    Booking.objects.create(
      ride=ride,
      first_name=form.cleaned_data["first_name"],
      last_name=form.cleaned_data["last_name"],
      email=form.cleaned_data["email"],
    )
    ride.seats_available -= 1
    ride.save()
    if ride.email:
      messages.success(
        request,
        f"Seat booked successfully! You can contact the driver at {ride.email}.",
      )
    else:
      messages.success(request, "Seat booked successfully! (Driver did not provide an email address.)")

  return redirect("rides:detail", ride_id=ride.id)


def offer(request):
  """Show the form on its own page for offering a new ride."""
  context = {
    "new_ride_form": NewRideForm(),
  }
  return render(request, "create_ride.html", context)


def create(request):
  if request.method == "POST":
    new_ride = NewRideForm(request.POST)
    if new_ride.is_valid():
      new_ride.save()
      messages.success(request, "Your ride has been added successfully.")
      return redirect("/rides")

    # If the form is invalid, show errors on the offer page
    messages.error(request, "Please correct the errors below to add your ride.")
    context = {"new_ride_form": new_ride}
    return render(request, "create_ride.html", context)

  # Non-POST requests just go back to main rides page
  return redirect("/rides")
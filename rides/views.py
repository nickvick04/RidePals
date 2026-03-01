from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from datetime import date, datetime

from .models import Person, Booking
from .forms import RideForm, NewRideForm, BookingForm, SignUpForm


def parse_location(location_string):
  """
  Parse a location string like "Los Angeles, CA" or "Los Angeles CA"
  Returns a tuple of (city, state) or (None, None) if invalid
  """
  if not location_string:
    return None, None

  location_string = location_string.strip()

  if ',' in location_string:
    parts = location_string.split(',')
    if len(parts) == 2:
      city = parts[0].strip()
      state = parts[1].strip().upper()
      return city, state

  parts = location_string.rsplit(None, 1)
  if len(parts) == 2:
    potential_state = parts[1].strip()
    if len(potential_state) == 2 and potential_state.isalpha():
      city = parts[0].strip()
      state = potential_state.upper()
      return city, state
    else:
      return location_string, None
  elif len(parts) == 1:
    part = parts[0].strip()
    if len(part) == 2 and part.isalpha():
      return None, part.upper()
    else:
      return part, None

  return None, None


# ── Public views ──────────────────────────────────────────────

def search(request):
  context = {}

  today = date.today()
  now_time = datetime.now().time()

  people = Person.objects.filter(
    Q(date__gt=today) | Q(date=today, time__gte=now_time)
  )

  if "origin" in request.GET or "destination" in request.GET or "date" in request.GET:
    context["inputExists"] = True

    origin_input = request.GET.get("origin", "").strip()
    destination_input = request.GET.get("destination", "").strip()
    date_input = request.GET.get("date", "").strip()

    origin_city, origin_state = parse_location(origin_input)
    destination_city, destination_state = parse_location(destination_input)

    if origin_city or origin_state:
      origin_filter = Q()
      if origin_city:
        origin_filter &= Q(origination_city__iexact=origin_city)
      if origin_state:
        origin_filter &= Q(origination_state__iexact=origin_state)
      people = people.filter(origin_filter)

    if destination_city or destination_state:
      destination_filter = Q()
      if destination_city:
        destination_filter &= Q(destination_city__iexact=destination_city)
      if destination_state:
        destination_filter &= Q(destination_state__iexact=destination_state)
      people = people.filter(destination_filter)

    if date_input:
      people = people.filter(date=date_input)

  context["people"] = people
  context["form"] = RideForm(request.GET or None)

  return render(request, "index_view.html", context)


def ride_detail(request, ride_id):
  """Show details for a single ride and its booking status."""
  ride = get_object_or_404(Person, id=ride_id)

  today = date.today()
  now_time = datetime.now().time()
  is_past = (ride.date < today) or (ride.date == today and ride.time < now_time)

  passengers = ride.bookings.order_by("booked_at")

  # Pre-fill booking form from logged-in user's profile
  booking_initial = {}
  if request.user.is_authenticated:
    booking_initial = {
      "first_name": request.user.first_name,
      "last_name": request.user.last_name,
      "email": request.user.email,
    }

  context = {
    "ride": ride,
    "is_past": is_past,
    "is_full": ride.seats_available <= 0,
    "passengers": passengers,
    "booking_form": BookingForm(initial=booking_initial),
  }
  return render(request, "ride_detail.html", context)


# ── Login-required views ──────────────────────────────────────

@login_required
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
    Booking.objects.create(
      user=request.user,
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
        f"Seat booked! You can contact the driver at {ride.email}.",
      )
    else:
      messages.success(request, "Seat booked successfully!")

  return redirect("rides:detail", ride_id=ride.id)


@login_required
def offer(request):
  """Show the form on its own page for offering a new ride."""
  initial = {
    "first_name": request.user.first_name,
    "last_name": request.user.last_name,
    "email": request.user.email,
  }
  context = {
    "new_ride_form": NewRideForm(initial=initial),
  }
  return render(request, "create_ride.html", context)


@login_required
def create(request):
  if request.method == "POST":
    new_ride = NewRideForm(request.POST)
    if new_ride.is_valid():
      ride = new_ride.save(commit=False)
      ride.user = request.user
      ride.save()
      messages.success(request, "Your ride has been posted successfully.")
      return redirect("/rides")

    messages.error(request, "Please correct the errors below.")
    context = {"new_ride_form": new_ride}
    return render(request, "create_ride.html", context)

  return redirect("/rides")


# ── Account views ─────────────────────────────────────────────

def signup(request):
  """Create a new account."""
  if request.user.is_authenticated:
    return redirect("/rides")

  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      messages.success(request, f"Welcome to RidePals, {user.first_name}!")
      return redirect("/rides")
  else:
    form = SignUpForm()

  return render(request, "accounts/signup.html", {"form": form})


@login_required
def my_rides(request):
  """Dashboard showing rides offered and bookings made by the logged-in user."""
  today = date.today()
  now_time = datetime.now().time()

  offered = Person.objects.filter(user=request.user).order_by("-date", "-time")
  booked = Booking.objects.filter(user=request.user).select_related("ride").order_by("-booked_at")

  # Annotate each ride/booking with is_past so the template doesn't need comparisons
  for ride in offered:
    ride.is_past = (ride.date < today) or (ride.date == today and ride.time < now_time)

  for booking in booked:
    r = booking.ride
    booking.ride_is_past = (r.date < today) or (r.date == today and r.time < now_time)

  return render(request, "accounts/my_rides.html", {
    "offered_rides": offered,
    "bookings": booked,
  })


@login_required
def cancel_booking(request, booking_id):
  """Cancel a booking made by the logged-in user."""
  booking = get_object_or_404(Booking, id=booking_id, user=request.user)

  if request.method == "POST":
    ride = booking.ride
    today = date.today()
    now_time = datetime.now().time()
    is_past = (ride.date < today) or (ride.date == today and ride.time < now_time)

    if is_past:
      messages.error(request, "You can't cancel a ride that has already departed.")
    else:
      ride.seats_available += 1
      ride.save()
      booking.delete()
      messages.success(request, "Your booking has been cancelled.")

  return redirect("my_rides")

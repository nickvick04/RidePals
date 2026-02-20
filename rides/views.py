from django.shortcuts import render
from django.db.models import Q

from .models import Person

# relative import of forms
from .forms import RideForm

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

  if "origin" in request.GET or "destination" in request.GET:
    context["inputExists"] = True
    
    origin_input = request.GET.get("origin", "").strip()
    destination_input = request.GET.get("destination", "").strip()
    
    # Parse the inputs
    origin_city, origin_state = parse_location(origin_input)
    destination_city, destination_state = parse_location(destination_input)
    
    # Start with all people
    people = Person.objects.all()
    
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

  return render(request, "search_view.html", context)
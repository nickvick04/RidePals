from django.shortcuts import render
from django.db.models import Q

from .models import Person

# relative import of forms
from .forms import RideForm

# Create your views here.


def index(request):
  context = {}
  return render(request, "index_view.html", context)


def search(request):
  context = {}

  if "origin_state" in request.GET or "destination_state" in request.GET:
    context["inputExists"] = True
    
    origin_state = request.GET.get("origin_state", "").strip().upper()
    destination_state = request.GET.get("destination_state", "").strip().upper()
    
    # Start with all people
    people = Person.objects.all()
    
    # Filter by origin state if provided
    if origin_state:
      people = people.filter(origination_state__iexact=origin_state)
    
    # Filter by destination state if provided
    if destination_state:
      people = people.filter(destination_state__iexact=destination_state)
    
    context["people"] = people

        
  context["form"] = RideForm()

  return render(request, "search_view.html", context)
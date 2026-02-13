from django.shortcuts import render

from .models import Person

# relative import of forms
from .forms import RideForm

# Create your views here.


def index(request):

  context = {}

  if "search" in request.GET:
    context["inputExists"] = True
    search = request.GET["search"].strip().upper()  # Convert to uppercase and strip whitespace
    
    # Search for people by origination_state or destination_state (case-insensitive)
    context["people"] = Person.objects.filter(origination_state__iexact=search) | Person.objects.filter(destination_state__iexact=search)

        
  context["form"] = RideForm()

  return render(request, "index_view.html", context)
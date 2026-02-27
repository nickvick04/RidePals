from django.urls import path
from . import views

app_name = "rides"

urlpatterns = [
    # /rides/
    path("", views.search, name="index"),

    # Optional alias: /rides/search/
    path("search/", views.search, name="search"),

    # Ride detail and booking
    path("<int:ride_id>/", views.ride_detail, name="detail"),
    path("<int:ride_id>/book/", views.book_seat, name="book"),

    # Page with the "offer a ride" form
    path("offer/", views.offer, name="offer"),

    # /rides/create/
    path("create/", views.create, name="create"),
]
from django.urls import path
from . import views

app_name = "rides"

urlpatterns = [
    # /rides/
    path("", views.search, name="search"),

    # Optional alias: /rides/search/
    path("search/", views.search),
]
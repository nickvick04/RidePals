from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from rides import views as ride_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Splash page at /
    path("", TemplateView.as_view(template_name="index.html"), name="home"),

    # How it works page
    path(
        "how-it-works/",
        TemplateView.as_view(template_name="how_it_works.html"),
        name="how_it_works",
    ),

    # Contact page
    path(
        "contact/",
        TemplateView.as_view(template_name="contact.html"),
        name="contact",
    ),

    # Auth: login/logout with our custom templates, signup and dashboard (custom)
    path("accounts/login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", ride_views.signup, name="signup"),
    path("accounts/my-rides/", ride_views.my_rides, name="my_rides"),

    # App lives at /rides/
    path("rides/", include("rides.urls")),
]

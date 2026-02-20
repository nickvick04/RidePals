from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Splash page at /
    path("", TemplateView.as_view(template_name="index.html"), name="home"),

    # App lives at /rides/
    path("rides/", include("rides.urls")),
]
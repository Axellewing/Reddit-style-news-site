from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("prod/", include("prod.urls")),
    path("admin/", admin.site.urls),
]
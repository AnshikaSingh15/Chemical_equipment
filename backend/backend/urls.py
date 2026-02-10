from django.urls import path, include

urlpatterns = [
    path("api/", include("analytics_app.urls")),
]


from django.urls import path
from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),  # root of app
    path("overview/", views.overview, name="analytics_overview"),
    path("predict/", views.predict, name="analytics_predict"),
]
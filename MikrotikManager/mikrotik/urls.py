from django.urls import path
from .views import MikIndex

urlpatterns = [
    path("", MikIndex, name="MikIndex"),
]
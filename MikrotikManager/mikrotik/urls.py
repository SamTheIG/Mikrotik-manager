from django.urls import path
from .views import MikIndex, MikManger

urlpatterns = [
        path("", MikIndex, name="MikIndex"),
        path("<str:mikrotik_name>/", MikManger, name="MikManger"),
    ]
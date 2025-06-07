from django.urls import path
from .views import MikIndex, MikManger, MikCommand

urlpatterns = [
        path("", MikIndex, name="MikIndex"),
        path("<str:mikrotik_name>/", MikManger, name="MikManger"),
        path("<str:mikrotik_name>/<str:Routercommand>/", MikCommand, name="MikCommand")
    ]
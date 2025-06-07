from django.urls import path
from .views import addMikuser, MikIndex, MikManger, MikCommand

urlpatterns = [
        path("", addMikuser, name="MikIndex"),
        path("addmikuser/", addMikuser, name="AddMikUser"),
        path("<str:mikrotik_name>/", MikManger, name="MikManger"),
        path("<str:mikrotik_name>/<str:Routercommand>/", MikCommand, name="MikCommand")
    ]
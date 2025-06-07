from django.shortcuts import render
from .models import Mikrotik

def MikIndex(request):
    Mikrotiks = Mikrotik.objects.all()
    context = {
        "Mikrotiks": Mikrotiks
    }
    return render(request, "mikrotik/index.html", context=context)
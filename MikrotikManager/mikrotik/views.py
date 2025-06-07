from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Mikrotik


@login_required
def MikIndex(request):
    if request.user.is_authenticated:
        user_id = request.user.id
    Mikrotiks = Mikrotik.objects.filter(Userid = user_id)
    context = {
        "Mikrotiks": Mikrotiks
    }
    return render(request, "mikrotik/index.html", context=context)
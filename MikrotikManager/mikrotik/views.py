from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Mikrotik


@login_required
def MikIndex(request):
    if request.user.is_authenticated: # TODO: what happens if user isn't authenticated?
        user_id = request.user.id
    Mikrotiks = Mikrotik.objects.filter(Userid = user_id)
    context = {
        "Mikrotiks": Mikrotiks
    }
    return render(request, "mikrotik/index.html", context=context)

@login_required
def MikManger(request, mikrotik_name):
    if request.user.is_authenticated: # TODO: what happens if user isn't authenticated?
        user_id = request.user.id
    Router = Mikrotik.objects.filter(Userid = user_id, MikName=mikrotik_name)
    Commands = ["\interface print", "\ip address print"]
    if Router:
        context = {
            "Mikrotik": Router,
            "Commands": Commands
        }
        return render(request, "mikrotik/manager.html", context=context)
    else:
        error = {
            "error": "The selected router does not exist?!\nIDK! go ask the admin!"
        }
        return render(request, "mikotik/index.html", context=error)
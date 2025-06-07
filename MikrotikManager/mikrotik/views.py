from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mikrotik
import paramiko


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
    router = Router[0].MikName
    Commands = ["interface Print", "ipAddress Print"]
    if Router:
        context = {
            "Mikrotik": router,
            "Commands": Commands
        }
        return render(request, "mikrotik/manager.html", context=context)
    else:
        error = {
            "error": "The selected router does not exist?!\nIDK! go ask the admin!"
        }
        return render(request, "mikotik/index.html", context=error)

@login_required
def MikCommand(request, mikrotik_name, Routercommand):
    if request.user.is_authenticated: # TODO: what happens if user isn't authenticated?
        user_id = request.user.id
    Router = Mikrotik.objects.filter(Userid = user_id, MikName=mikrotik_name)
    router = Router[0]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=router.MikIp, port=router.MikPort,
                username=router.MikUsername, password=router.MikPassword, look_for_keys=False)
    command = "\\" + Routercommand
    print(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    res = stdout.read().decode()
    print(res)
    ssh.close()
    result = {
        "result": res
    }
    return render(request, "mikrotik/manager.html", context=result)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mikrotik, Hotspot
from .forms import addMikuserForm
import paramiko



def save_user_date(name, username, password, profile, limit_in, limit_out, ip, port):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=ip, port=port, username=username, password=password, look_for_keys=False)
        stdin, stdout, stderr = ssh.exec_command(f"""/ip hotspot user set [find name={name}]
                         name={username} password={password} profile={profile} limit-bytes-in={limit_in} limit-bytes-out={limit_out}""")
        res = stdout.read().decode()
        ssh.close()
        return res
        # TODO: send a seccess message to user
    except Exception as e:
        # TODO: send a failed message to user
        pass


@login_required
def addMikuser(request):
    if request.method == "POST":
        if request.method == 'POST':
            form = addMikuserForm(request.POST, user=request.user)
            username = request.POST.get('username')
            password = request.POST.get('password')
            speed = request.POST.get('speed')
            upload = request.POST.get('upload')
            download = request.POST.get('download')
            if form.is_valid():
                router = form.cleaned_data['device']
            else:
                user_id = request.user.id
                router = Mikrotik.objects.filter(Userid=user_id)[0]
            Hotspot.objects.create(
                Hotspot_id = router,
                uname = username,
                upass = password,
                speed = speed,
                upload = upload,
                download = download
            )
            save_user_date(router.MikName, username, password, speed, download, upload, router.MikIp, router.MikPort) #TODO: ip and port
            return redirect("/")
    else:
        user_id = request.user.id
        routers = Mikrotik.objects.filter(Userid=user_id)
        if len(routers) == 0:
            return redirect("/")
        elif len(routers) == 1:
            return render(request, "mikrotik/addMikuser.html")
        else:
            form = addMikuserForm(user=request.user)
            context = {
                "form": form,
                "routers": routers
            }
            # TODO: Create comboBox for Speed, Download, Upload
            return render(request, "mikrotik/addMikuser.html", context=context)


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
    Commands = ["interface print", "ip address print"]
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
    command = "/" + Routercommand
    stdin, stdout, stderr = ssh.exec_command(command)
    res = stdout.read().decode()
    ssh.close()
    result = {
        "result": res
    }
    return render(request, "mikrotik/manager.html", context=result)


from django.shortcuts import render,redirect
from rbac.models import User
from rbac.service.init_permission import init_permission
# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    elif request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('pass')
        user_obj = User.objects.filter(name=username,password=password)
        if not user_obj:
            return render(request,"login.html")
        else:
            init_permission(request,user_obj)
            return redirect('/index/')
def index(request):
    return render(request,'index.html')
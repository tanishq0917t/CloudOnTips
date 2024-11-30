from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
from .tasks import create_EC2
from .models import vps_details

def dashboard(request):
    return render(request,'dashboard/dashboard.html',{'user':request.session.get('user')})

def newVps(request):
    return render(request,'dashboard/newVps.html',{'user':request.session.get('user')})

def serverless(request):
    return render(request,'dashboard/serverless.html',{'user':request.session.get('user')})

def myvps(request):
    vps=vps_details.objects.filter(user=request.session.get('user'))
    print(vps)
    return render(request,'dashboard/myvps.html',{'user':request.session.get('user'),'vps':vps})

def configureNewVPS(request):
    if request.method=="POST":
        data={
            'serverName':request.POST['name'],
            'serverStorage':request.POST['storage'],
            'serverOS':request.POST['os'],
            'serverType':request.POST['inst'],
            'serverSoftwares':request.POST.getlist('list[]'),
            'user':request.session.get('user')
        }
        idd=create_EC2.delay(data).id
        vps=vps_details(name=request.POST['name'],storage=request.POST['storage'],os=request.POST['os'],type=request.POST['inst'],user=request.session.get('user'),task_id=idd,status='Initializing')
        vps.save()
        return JsonResponse({'status':os.getenv('ACCESS_KEY'),'message':idd})
    else:
        return JsonResponse({'status':'error','message':'Not Done'})
    

def pems(request):
    return render(request,'dashboard/pems.html',{'user':request.session.get('user')})

def getPemNames(request):
    if request.method=="POST":
        user=request.session.get('user')
        pems=list(vps_details.objects.filter(user=user).values())
        print(pems)
        return JsonResponse({'pems':pems})
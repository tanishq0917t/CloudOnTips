from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
from .tasks import create_EC2

def dashboard(request):
    return render(request,'dashboard/dashboard.html',{'user':request.session.get('user')})

def newVps(request):
    return render(request,'dashboard/newVps.html',{'user':request.session.get('user')})

def serverless(request):
    return render(request,'dashboard/serverless.html',{'user':request.session.get('user')})

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
        #Write the code to fetch form and initiate a celery task
        return JsonResponse({'status':os.getenv('ACCESS_KEY'),'message':idd})
    else:
        return JsonResponse({'status':'error','message':'Not Done'})
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os

def dashboard(request):
    return render(request,'dashboard/dashboard.html',{'user':request.session.get('user')})

def newVps(request):
    return render(request,'dashboard/newVps.html',{'user':request.session.get('user')})

def serverless(request):
    return render(request,'dashboard/serverless.html',{'user':request.session.get('user')})

def configureNewVPS(request):
    if request.method=="POST":
        print(request.POST.getlist('list[]'))
        #Write the code to fetch form and initiate a celery task
        return JsonResponse({'status':os.getenv('ACCESS_KEY'),'message':os.getenv('SECRET_KEY')})
    else:
        return JsonResponse({'status':'error','message':'Not Done'})
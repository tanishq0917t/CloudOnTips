from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

def dashboard(request):
    return render(request,'dashboard/dashboard.html',{'user':request.session.get('user')})

def newVps(request):
    return render(request,'dashboard/newVps.html',{'user':request.session.get('user')})

def serverless(request):
    return render(request,'dashboard/serverless.html',{'user':request.session.get('user')})

def configureNewVPS(request):
    if request.method=="POST":
        print(request.POST.getlist('list[]'))
        #Write the code to fetch form 
        return JsonResponse({'status':'success','message':'Done'})
    else:
        return JsonResponse({'status':'error','message':'Not Done'})
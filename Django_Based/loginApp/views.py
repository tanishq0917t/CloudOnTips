from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .tasks import send_html_email
from django.http import HttpResponse
import random

def index(request):
    if request.session.get('user'):
        return redirect('dashboard')
    if request.session.get('error'):
        error=request.session.get('error')
        request.session['error']=None
        return render(request,'loginApp/login.html',{'error':error})
    return render(request,'loginApp/login.html')

def otp(request):
    if request.session.get('otp_required')==True:
        request.session['otp_required']=False
        return render(request,'loginApp/otp.html')
    if request.method=="POST": 
        if request.session.get('otp_for_verification'):
            userOTP=int(request.POST['otp'])
            sessionOTP=request.session['otp_for_verification']
            if userOTP==sessionOTP:
                request.session['otp_for_verification']=None
                request.session['user']='tanishq091710'
                return redirect('dashboard')
            else:
                request.session['otp_for_verification']=None
                request.session['error']='Invalid OTP, Please login again'
                return redirect('index')
        else:
            return HttpResponse("Unathorized Access")
    else: #Unauthorized access
        return redirect('index')

def _login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            request.session['otp_required'] = True
            otp=random.randint(100000,999999)
            request.session['otp_for_verification']=otp
            print(f"Generated OTP: {otp}")
            send_html_email.delay(otp)
            return redirect('/otp') 
        else:
            return redirect('index')  
    return render(request, 'login.html')


def _logout(request):
    request.session['user']=None
    return redirect('index')
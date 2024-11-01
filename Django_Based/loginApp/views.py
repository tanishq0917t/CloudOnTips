from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .tasks import send_html_email
from django.http import HttpResponse
import random
from django.contrib import messages


def index(request):
    if request.session.get('user'):
        return redirect('dashboard')
    return render(request, 'loginApp/login.html')

def otp(request):
    if request.session.get('otp_required') == True:
        request.session['otp_required'] = False
        return render(request, 'loginApp/otp.html')
    if request.method == "POST": 
        if request.session.get('otp_for_verification'):
            userOTP = int(request.POST['otp'])
            sessionOTP = request.session['otp_for_verification']
            if userOTP == sessionOTP:
                request.session['otp_for_verification'] = None
                request.session['user'] = request.session.get('otp_username')
                request.session['otp_username'] = None
                return redirect('dashboard')
            else:
                request.session['otp_for_verification'] = None
                messages.error(request, 'Invalid OTP, Please login again')
                return redirect('index')
        else:
            return HttpResponse("Unauthorized Access")
    else:  # Unauthorized access
        return redirect('index')

def _login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['otp_required'] = True
            otp=random.randint(100000,999999)
            request.session['otp_for_verification']=otp
            request.session['otp_username']=username
            print(f"Setting username for otp: {request.session['otp_username']}")
            print(f"Generated OTP: {otp}")
            email=User.objects.get(username=username).email
            send_html_email.delay(otp,email)
            return redirect('/otp') 
        else:
            messages.error(request, 'Invalid Credentials, Please login again')
            return redirect('index')  
    return render(request, 'login.html')


def _logout(request):
    request.session['user']=None
    return redirect('index')
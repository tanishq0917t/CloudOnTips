from django.urls import path
from .views import index,_login,otp,_logout

urlpatterns = [
    path('',index,name='index'),
    path('login/',_login,name='login'),
    path('otp',otp,name='otp'),
    path('logout',_logout,name='logout')
]

from django.urls import path
from .views import dashboard,newVps,configureNewVPS,serverless,myvps

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('newVps',newVps,name='newVps'),
    path('myvps',myvps,name='myvps'),
    path('configureNewVPS',configureNewVPS,name='configureNewVPS'),
    path('serverless',serverless,name='serverless')
]

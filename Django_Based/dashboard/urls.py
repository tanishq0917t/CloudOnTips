from django.urls import path
from .views import dashboard,newVps,configureNewVPS,serverless

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('newVps',newVps,name='newVps'),
    path('configureNewVPS',configureNewVPS,name='configureNewVPS'),
    path('serverless',serverless,name='serverless')
]

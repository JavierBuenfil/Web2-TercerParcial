
from django.urls import path

from . import views

urlpatterns = [
    path('client/login',views.login,name='login'),
    path('generate_password/<str:password>',views.makepassword,name='makepassword'),
    path('client/list',views.list,name='list'),
    path('vista/',views.vista,name='vista')
]

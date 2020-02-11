from django.urls import path
from . import views

urlpatterns =[
    path('',views.home,name='home'),
    path('mult',views.mult,name='mult')
]

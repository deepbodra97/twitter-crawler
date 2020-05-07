from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [

    path('', views.index),
    path('search/', views.search),
]

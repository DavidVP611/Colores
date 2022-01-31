from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('code/', views.codeQR),
    path('readQR/', views.readQR),
    path('createQR/', views.createQR),
]
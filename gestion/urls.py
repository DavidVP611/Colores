from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('readQR/', views.readQR),
    path('createQR/', views.createQR),
]
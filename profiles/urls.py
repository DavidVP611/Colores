from django.urls import path
from . import views

urlpatterns = [
    path('text/', views.view_text),
    path('read_text/', views.read_text),
]
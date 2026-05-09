from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('safe/', views.safe, name='safe'),
]
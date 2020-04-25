from django.urls import path, include
from . import views 

urlpatterns = [
path('', views.index),
path('message/<str:message>',views.api),
]


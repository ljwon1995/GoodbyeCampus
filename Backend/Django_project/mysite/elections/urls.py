from django.urls import path, include
from . import views 

urlpatterns = [
path('', views.index),
path('message/<str:message>',views.api),
path('course',views.course),
path('delete',views.delete),
path('add',views.add)
]


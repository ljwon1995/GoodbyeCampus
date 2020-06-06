from django.urls import path, include
from . import views 

urlpatterns = [
path('', views.index),
path('message/<str:message>',views.api),
path('course/<str:year>/<str:sem>/<str:main>/<str:sub>',views.course),
path('delete',views.delete),
path('add',views.add)
]


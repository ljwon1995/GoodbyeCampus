from django.urls import path, include
from . import views 

urlpatterns = [
path('', views.index),
path('areas/<str:area>/',views.areas),
path('areas/<str:area>/results/',views.results),
path('polls/<int:poll_id>',views.polls),
path('candidates/<str:name>',views.candidates)
]


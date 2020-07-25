from django.urls import path
from . import views
from . import worldmap

app_name = 'worldmap'

urlpatterns = [
    path('', views.index, name='index')
]

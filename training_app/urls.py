from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('', views.machine, name='home'),

]
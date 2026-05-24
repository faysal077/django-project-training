from django.urls import path
from . import views

app_name = "employee_list"

urlpatterns = [
    path('', views.employee_search, name='home'),
]


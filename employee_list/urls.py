from django.urls import path
from . import views

app_name = "employee_list"

urlpatterns = [
    path('', views.employee_search, name='home'),
    path(
        "edit/<int:pk>/",
        views.employee_edit,
        name="employee_edit"
    ),
]


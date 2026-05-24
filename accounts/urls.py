from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
]

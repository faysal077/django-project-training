from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_dashboard, name='home'),
    path('by-name/', views.search_by_name, name='search_by_name'),
    path('by-training/', views.search_by_training, name='search_by_training'),
    path('unattended/', views.search_not_taken, name='search_not_taken'),
    path('by-multiple/', views.search_by_multiple_trainings, name='search_by_multiple_trainings'),
]

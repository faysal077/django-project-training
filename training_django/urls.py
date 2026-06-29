"""
URL configuration for training_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from training_app import views

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', include('accounts.urls')),

    path('', include('django_prometheus.urls')),

    path('', lambda request: redirect(
        'accounts:login'
    ) if not request.user.is_authenticated
      else redirect('dashboard:index')),

    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('search/', include('search.urls', namespace='search')),
    path('employee-list/', include('employee_list.urls', namespace='employee_list')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


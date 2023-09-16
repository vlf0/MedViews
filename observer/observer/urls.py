"""
URL configuration for observer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from WebApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dept, name='dept'),
    # path('errors.css/', views.errors.css, name='errors.css'),
    path('ref_to_type/', views.ref_to_type, name='ref_to_type'),
    path('<str:chosen_dept>/research_type/', views.research_type, name='research_type'),
    path('<str:chosen_dept>/', views.ref_to_output, name='ref_to_output'),
    path('<str:chosen_dept>/<str:chosen_type>/<str:from_dt>:<str:to_dt>/', views.output, name='output'),
    path('api/testing/javascript/', views.api_func, name='api_func'),
]

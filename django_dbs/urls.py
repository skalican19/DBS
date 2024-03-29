"""django_dbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from dbs_zadanie import views


urlpatterns = [
    path('', views.index),
    path('v1/health/', views.uptime),
    path('v1/ov/submissions/', views.submissions),
    path('v1/ov/submissions/<int:sub_id>', views.delete),
    path('v1/companies/', views.companies),
    path('v2/ov/submissions/', views.v2_submissions),
    path('v2/ov/submissions/<int:sub_id>', views.v2_submissions_url_with_id),
    path('v2/companies/', views.v2_companies)
]

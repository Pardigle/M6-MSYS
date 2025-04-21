"""
URL configuration for MyInventorySystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("view_bottles/", views.view_bottles, name="view_bottles"),
    path("view_bottle_details/<int:pk>/", views.view_bottle_details, name="view_bottle_details"),
    path("view_supplier", views.view_supplier, name="view_supplier"),
    path("add_bottle", views.add_bottle, name="add_bottle"),
    path("logout/", views.logout_view, name="logout"),
    ]

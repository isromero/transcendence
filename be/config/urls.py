"""
URL configuration for transcendence project.

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
from django.urls import path, include
from apps.core.views.auth import auth_login, auth_callback, auth_logout, wololo

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
	path("auth/login/", auth_login, name="auth_login"),
    path("auth/callback/", auth_callback, name="auth_callback"),
    path("auth/logout/", auth_logout, name="auth_logout"),
    path("auth/wololo/", wololo, name="wololo"),
]


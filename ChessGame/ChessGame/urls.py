"""
URL configuration for ChessGame project.

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
from django.urls import path
from register import views

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('registersuccess/',views.reg_success,name="registerSuccess"),
    
    path('home/',views.home,name="home"),
    path('logout/',views.logout,name="logout"),
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('forgot_password/',views.forgot_password,name="forgot_password"),
    path('error_404/',views.error_404,name="error_404"),
    path('charts/',views.charts,name="charts"),
    path('tables/',views.tables,name="tables"),
]

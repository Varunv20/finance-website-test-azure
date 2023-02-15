"""azureproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from django.contrib import admin
from django.urls import path, include
from restaurant_review import views as user_view
from django.contrib.auth import views as auth

from .router import router

urlpatterns = [

    path('admin/', admin.site.urls),


    #####user related path##########################
    path('', include('restaurant_review.urls')),
    path('login/', user_view.Login, name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='restaurant_review/index.html'), name='logout'),
    path('register/', user_view.register, name='register'),
    path('profile', user_view.sign_in, name='sign_in'),
    path('dashboard', user_view.create_account, name='create_account'),
    path('', user_view.logout_view, name='logout'),
    path('password_reset/done/', auth.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/done/', auth.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth.PasswordResetConfirmView.as_view(template_name="main/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), name='password_reset_complete'), 
    path("password_reset", user_view.password_reset_request, name="password_reset")

]

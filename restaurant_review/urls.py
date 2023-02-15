from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in', views.create_signin_page, name='sign_in_page'),
    path('create_account', views.create_account_page, name='create_account_page'),


    path('profile', views.sign_in, name='sign_in'),
    path('dashboard/', views.create_account, name='create_account'),
    path('', views.logout_view, name='logout'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), name='password_reset_complete'), 
    path("password_reset", views.password_reset_request, name="password_reset")

    
    

]

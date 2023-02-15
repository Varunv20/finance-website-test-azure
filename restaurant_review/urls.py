from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in', views.create_signin_page, name='sign_in_page'),
    path('create_account', views.create_account_page, name='create_account_page'),


    path('profile', views.create_profile, name='user_profile'),
    path('dashboard/', views.create_account, name='create_account'),

]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
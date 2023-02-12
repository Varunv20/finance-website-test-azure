from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in/', views.create_signin_page, name='sign_in_page'),
    path('create_account', views.create_account_page, name='create_account_page'),

    path('dashboard/', views.sign_in, name='sign_in'),
    path('dashboard/', views.create_account, name='create_account'),

]
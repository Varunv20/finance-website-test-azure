from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.create_signin_page, name='sign_in_page'),
    path('', views.create_account_page, name='create_account_page'),

    path('add', views.sign_in, name='sign_in'),
    path('create', views.create_account, name='create_account'),

]
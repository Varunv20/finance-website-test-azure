from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.details, name='details'),
    path('add', views.sign_in, name='sign_in'),
    path('create', views.create_account, name='create_account'),

    path('review/<int:id>', views.add_review, name='add_review'),
]
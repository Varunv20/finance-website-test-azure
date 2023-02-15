import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    UserID = models.IntegerField()

   
    phone_number = models.CharField(max_length=20)
    birth_date = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    transactions = models.JSONField()
    products_owned = models.JSONField()
    account_balance = models.DecimalField(max_digits=15, decimal_places=2)
    payment_info = models.JSONField()




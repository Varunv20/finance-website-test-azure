import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class User(models.Model):
    UserID = models.IntegerField()

    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    birth_date = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    transactions = models.JSONField()
    products_owned = models.JSONField()
    account_balance = models.DecimalField(max_digits=15, decimal_places=2)
    payment_info = models.JSONField()




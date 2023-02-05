import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.CharField(max_length=500)
    review_date = models.DateTimeField('review date')    
    def __str__(self):
        return self.restaurant.name + " (" + self.review_date.strftime("%x") +")"
class user(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
class get_user_data(models.Model):
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






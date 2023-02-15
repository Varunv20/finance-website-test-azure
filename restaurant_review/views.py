from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count
from django.urls import reverse
from django.utils import timezone
from restaurant_review.models import User
from django.contrib import messages
import psycopg2
from psycopg2 import Error
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth import logout

import os
import json 
import random
def index(request):
    print('Request for index page received')

   
    return render(request, 'restaurant_review/index.html')

def create_profile(request):
    print('Request for signin page received')

 

    return render(request, 'restaurant_review/profile.html')
def create_signin_page(request):
    print('Request for signin page received')

 

    return render(request, 'restaurant_review/login.html')



def create_account_page(request):
    print('Request for add sign-in page received')

    return render(request, 'restaurant_review/create_account.html')

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_server_connection():
     
    connection = None
    try:
        conn = psycopg2.connect(database=os.getenv("DBUSER"),
                            user=os.getenv("DBUSER"),
                            password=os.getenv("DBPASS"),
                            host=os.getenv("DBHOST"),
                            port="5432")
        connection = psycopg2.connect(user=os.getenv("DBUSER"),
                                  password=os.getenv("DBPASS"),
                                  host=os.getenv("DBHOST"),
                                  port="5432",
                                  database="postgres_db")
        print("Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection



def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    DATABASE_URL = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL)
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

class user_data:
    def __init__(self):
        return
    def verify(self,connection):
        self.account_id = ""
    def verify_and_populate(self,connection,user_model):
        query = f"SELECT * FROM Users WHERE Username = '{user_model.username}'"
        user1 = connection.read_query(query)[0]
        if not user1[2] == user_model.password:
            return False
        user_model.UserID = user1[0] 
        user_model.account_balance = user1[7]  
        user_model.products_owned = user1[11]
        user_model.location  = user1[5]
        user_model.phone_number = user1[6]
        user_model.email = user1[9]
        user_model.transactions =  user1[8]
        user_model.payment_info =  user1[12]
        user_model.birth_date =  user1[10]
        user_model.f_name =  user1[4] 
        user_model.l_name =  user1[3]
        return True
    def create_account(self,connection, user):
        location = user.city + " " + user.country
        query = f"INSERT INTO Users (UserID, Username, Paswsword , LastName ,  FirstName ,Location ,  PhoneNumber ,   AccountBalance , Transactions , Email , BirthDate , ProductsOwned , PaymentInfo) VALUES ('{user.id}','{user.username}','{user.password}','{user.l_name}','{user.f_name}','{location}',{user.phone_number},{user.account_balance},{json.dumps(user.transactions)},{user.email},{user.birth_date},{json.dumps(user.products_owned)},{json.dumps(user.payment_info)},)"

def username_exists(conn, username):
    query = f"SELECT * FROM Users WHERE Username = '{username}'"
    ret = conn.read_query
    if len(ret) == 0:
        return False
    return True
def create_id(conn):
    id1 = random.randint(0, 2**32)
    query = f"SELECT * FROM Users WHERE UserID = '{id1}'"
    ret = conn.read_query(query)
    if len(ret) == 0:
        return id1 
    create_id(conn)
    




def logout_view(request):
    logout(request)
    return render(request, 'restaurant_review/index.html')
    
def create_restaurant(request):
    print('Request for add restaurant page received')

    return render(request, 'restaurant_review/create_restaurant.html')
@login_required(login_url='/login')
def login(request, user):
    
    return render(request, 'restaurant_review/dashboard.html')
def reset_password(request):
    username = request.POST['username']
    password = request.POST['password']
    u = User.objects.get(username=username)
    u.set_password("password")
def sign_in(request):
    print("signing in")
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.info(request, 'Invalid Username Or Password')
            

    except (KeyError):
        # Redisplay the question voting form.
        return render(request, 'restaurant_review/index.html', {
            'error_message': "An Error Occured",
        })
  

    

def create_account(request):
    try:
        print("creating account...")

        user1 = User.objects.create_user(request.POST['username'], request.POST['email'],  request.POST['password'])
       
       
        user1.password = request.POST['password']
        user1.birth_date = request.POST['birth-date']
        user1.phone_number = request.POST['phone']
        user1.first_name = request.POST['f_name']
        user1.last_name = request.POST['l_name']
        user1.city = request.POST['city']
        user1.country = request.POST['country']
        user1.account_balance = 0
        user1.transactions = {}
        user1.products_owned = {}
        user1.payment_info = {}
        




    except (KeyError):
        messages.info(request, 'Invalid Data')
        print("an error occured while creating account")
        return render(request, 'restaurant_review/index.html', {
            'error_message': "An Error Occured",
        })
    else:

        user1.save() 
        login(user1)
        return
        #print("account_created") 
       # return HttpResponseRedirect(reverse('details', args=(user1.id,)))


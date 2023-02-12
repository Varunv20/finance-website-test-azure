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
import os
import json 
import random
def index(request):
    print('Request for index page received')

   
    return render(request, 'restaurant_review/index.html')


def create_signin_page(request, id):
    print('Request for signin page received')

 

    return render(request, 'restaurant_review/sign_in.html')



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
        print("MySQL Database connection successful")
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
    
class db_connection:
    def __init__(self):
       self.connection = create_server_connection() 
    def create_table(self):
        table = """
        CREATE TABLE Users (
            UserID int,
            Username varchar(255),
            Paswsword varchar(255),
            LastName varchar(255),
            FirstName varchar(255),
            Location varchar(255),
            PhoneNumber int,
            AccountBalance money,
            Transactions varchar(255),
            Email varchar(255),
            BirthDate varchar(255),
            
            ProductsOwned varchar(255),
            PaymentInfo varchar(255)
        );
        """
        self.execute_query(table)
    def execute_query(self, query, values=None):
        connection = self.connection
        cursor = connection.cursor(buffered=True)
        try:
            if values == None:
                cursor.execute(query)
            else:
                cursor.execute(query,values)
            connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")

    def read_query(self, query, values=None):
        connection = self.connection
        cursor = connection.cursor(buffered=True)
        result = None
        try:
            if values == None:
                cursor.execute(query)
            else:
                cursor.execute(query,values)
            connection.commit()

            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")




def create_restaurant(request):
    print('Request for add restaurant page received')

    return render(request, 'restaurant_review/create_restaurant.html')


@csrf_exempt
def sign_in(request):
    try:
        username = request.POST['username']
        password = request.POST['password']

    except (KeyError):
        # Redisplay the question voting form.
        return render(request, 'restaurant_review/add_restaurant.html', {
            'error_message': "Invalid Username Or Password",
        })
    else:
        db_conn = db_connection()
        user1_data = user_data()
        user1 = User()
        user1.name = username
        user1.street_address = password
        correct_sign_in = user1_data.verify_and_populate(db_conn, user1) 
        if not correct_sign_in:
            messages.info(request, 'Invalid Username Or Password')
            return render(request, 'restaurant_review/add_restaurant.html', {
            'error_message': "Invalid Username Or Password",
        })
        User.save(user1)  
        return HttpResponseRedirect(reverse('details', args=(user1.id,)))

    

def create_account(request):
    try:
        user1 = User()
        db_conn = db_connection()
        user1.username = username = request.POST['username']
        u_exists = username_exists(db_conn, username) 
        if u_exists:
           messages.info(request, 'Username Taken')
           return 
        user1.UserID = create_id(db_conn) 
        user1.password = request.POST['password']
        user1.birth_date = request.POST['birth-date']
        user1.phone_number = request.POST['phone']
        user1.email = request.POST['email']
        user1.f_name = request.POST['f_name']
        user1.l_name = request.POST['l_name']
        user1.city = request.POST['city']
        user1.country = request.POST['country']
        user1.account_balance = 0
        user1.transactions = {}
        user1.products_owned = {}
        user1.payment_info = {}





    except (KeyError):
        messages.info(request, 'An Error Occured')

        return render(request, 'restaurant_review/add_restaurant.html', {
            'error_message': "Invalid Data",
        })
    else:

        user1_data = user_data()
        user1_data.create_account(db_conn, user1)
        User.save(user1)  
        return HttpResponseRedirect(reverse('details', args=(user1.id,)))


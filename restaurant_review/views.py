from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate

import psycopg2
from psycopg2 import Error
from django.contrib import admin
from .models import User
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

import os
import json 
import random

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system ####################################
            htmly = get_template('user/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'Create Account', 'varunviges191@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            messages.success(request, f'Your account has been created ! You are now able to log in')
            user1 = User.objects.create_user(form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password'))
       
       
            user1.password = form.cleaned_data.get('password')
            user1.birth_date = form.cleaned_data.get('birth-date')
            user1.phone_number =form.cleaned_data.get('phone')
            user1.first_name = form.cleaned_data.get('f_name')
            user1.last_name = form.cleaned_data.get('l_name')
            user1.city = form.cleaned_data.get('city')
            user1.country = form.cleaned_data.get('country')
            user1.account_balance = 0
            user1.transactions = {}
            user1.products_owned = {}
            user1.payment_info = {}
            user1.save()
            return redirect('/profile')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form, 'title':'register here'})
  
################ login forms###################################################
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form, 'title':'log in'})
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "restaurant_review/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'https://msdocs-python-postgres-1ab.azurewebsites.net',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'varunviges191@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})
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
#@login_required(login_url='/login')
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


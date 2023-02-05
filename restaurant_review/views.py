from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count
from django.urls import reverse
from django.utils import timezone
from restaurant_review.database_funcs import database_funcs
from restaurant_review.models import Users, get_user_data, Restaurant, Review
from django.contrib import messages
# Create your views here.

def index(request):
    print('Request for index page received')

    restaurants = Restaurant.objects.annotate(avg_rating=Avg('review__rating')).annotate(review_count=Count('review'))
    return render(request, 'restaurant_review/index.html', {'restaurants': restaurants })


def account_dashboard(request, id):
    print('Request for restaurant details page received')

    restaurant = get_object_or_404(Restaurant, pk=id)


    return render(request, 'restaurant_review/details.html', {'restaurant': restaurant})



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
        db_conn = database_funcs.db_connection()
        user1_data = database_funcs.user_data()
        user1 = Users()
        user1.name = username
        user1.street_address = password
        correct_sign_in = user1_data.verify_and_populate(db_conn, user1) 
        if not correct_sign_in:
            messages.info(request, 'Invalid Username Or Password')
            return render(request, 'restaurant_review/add_restaurant.html', {
            'error_message': "Invalid Username Or Password",
        })
        Users.save(user1)  
        return HttpResponseRedirect(reverse('details', args=(user1.id,)))

    

def create_account(request):
    try:
        user1 = Users()
        db_conn = database_funcs.db_connection()
        user1.username = username = request.POST['username']
        u_exists = database_funcs.username_exists(db_conn, username) 
        if u_exists:
           messages.info(request, 'Username Taken')
           return 
        user1.UserID = database_funcs.create_id(db_conn) 
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

        user1_data = database_funcs.user_data()
        user1_data.create_account(db_conn, user1)
        Users.save(user1)  
        return HttpResponseRedirect(reverse('details', args=(user1.id,)))

@csrf_exempt
def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    try:
        user_name = request.POST['user_name']
        rating = request.POST['rating']
        review_text = request.POST['review_text']
    except (KeyError):
        #Redisplay the question voting form.
        return render(request, 'restaurant_review/add_review.html', {
            'error_message': "Error adding review",
        })
    else:
        review = Review()
        review.restaurant = restaurant
        review.review_date = timezone.now()
        review.user_name = user_name
        review.rating = rating
        review.review_text = review_text
        Review.save(review)
                
    return HttpResponseRedirect(reverse('details', args=(id,)))        
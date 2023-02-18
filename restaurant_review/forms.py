
from django import forms
from  .models import User_Model
from django.contrib.auth.forms import UserCreationForm
 
 
 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length = 20)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    birth_date = forms.CharField(max_length=20)
    city = forms.CharField(max_length=20)
    country = forms.CharField(max_length=20)
    
    class Meta:
        model = User_Model
        fields = ['username', 'email', 'phone_no', 'password1', 'password2','first_name','last_name', 'birth_date','city','country']
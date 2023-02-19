
from django import forms
from  .models import User_Model
from django.contrib.auth.forms import UserCreationForm
 
 
 
class UserRegisterForm(UserCreationForm):
    username =forms.CharField(max_length = 20) 
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    email = forms.EmailField()
    phone_no = forms.IntegerField()
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    birth_date = forms.DateField()
    city = forms.CharField(max_length=20)
    country = forms.CharField(max_length=20)
    
   
    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','country' ,'whatsapp_number','password1','password2']

class Password(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password1' , 'password2' , 'password3']
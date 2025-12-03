from django import forms
from django.contrib.auth import login, authenticate  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=70)
    // password = 

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

from django import forms
from .models import *

class UserLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'UserName'}))


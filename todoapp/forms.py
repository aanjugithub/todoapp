from django import forms
from django.forms import Form

from django.contrib.auth.models import User  #import User model

from todoapp.models import Todos

from django.contrib.auth.forms import UserCreationForm #where usercreation forms where created cntrl+clik to see the implimentation

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]  #2 pass are provided for checking which are comin from user creation

#login form
class LoginForm(forms.Form):
  
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
   

#inherit from model forms when we need a save or udate in db side


class ToDoForm(forms.ModelForm):
    class Meta:
        model=Todos #import 
        fields=["name"]

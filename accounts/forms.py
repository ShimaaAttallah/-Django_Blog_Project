from time import time
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
 
class signUpForm(UserCreationForm):
    email = forms.CharField(max_length=225,required=True,widget=forms.EmailInput(),help_text='ex: iti@gmail.com')
    
    class Meta:
        model=User
        fields = {'username','email','password1','password2'}
        #field_order = ['username', 'email','password1','password2']
         
class loginForm(AuthenticationForm):
    
    class Meta:
        model=User
        fields = {'username','password'}
        #field_order = ['username', 'email','password1','password2']
         

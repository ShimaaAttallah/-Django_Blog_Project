from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login,authenticate
from django.urls import reverse, reverse_lazy

from discussion.models import Post
from .forms import signUpForm,loginForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from django.views.generic import UpdateView

# Create your views here.
def signup(request):
    form = signUpForm()
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('homepage')
    return render(request,'signup.html',{'form':form})

class UserUpdateView(UpdateView):
    model=User
    fields = ('first_name','last_name','email','username')
    template_name = 'my_profile.html'
    success_url = reverse_lazy('my_profile')
    def get_object(self):
        return self.request.user

def login(request):
    form = loginForm()
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
       
        user = authenticate(request, username=username, password=password)
        
        print(user.is_active)
        if user is not None:
            if not user.is_active :
                return render(request, 'login.html',{'blog':"BLOCKED",'form':form})
            auth_login(request, user)
            return redirect('homepage')
          
        else:
            return redirect('/login')

    return render(request, 'login.html',{'blog':"BLOCKED",'form':form})

def user_login(request):
        form = loginForm()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
    
            # user = authenticate(username = username, password = password)
            user = authenticate(request, username = username, password = password)
    
            if user:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('homepage')
                elif user.is_active == False:
                    return render(request, 'login.html',{'blog':"BLOCKED",'form':form})
                #return HttpResponse("Account Not Active")
            else:
                print("Someone tried to login and failed")
                print(f"Username: {username} and password {password}")
                return render(request, 'login.html',{'blog':"User Name or Password is wrong",'form':form})
                #return HttpResponse ("Invalid Login details supplied")
        
        else:
            return render(request, 'login.html',{'form':form})
        
        
  
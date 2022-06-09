from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CreateUserForm,LoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL

def signupView(request,*args,**kwargs):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username,password=password)
            login(request,user)

            return redirect("tweet:tweetlist")

    context = {
        "form" : form
    }

    return render(request,'accounts/signup.html',context)


def loginView(request,*args,**kwargs):
    form = LoginForm(request,data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request,user)
        return redirect("tweet:tweetlist")

    context = {
        "form":form
    }
    return render(request,'accounts/login.html',context)

def logoutView(request,*args,**kwargs):
    logout(request)
    return redirect("base")
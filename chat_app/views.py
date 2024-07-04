from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,"home_page.html")


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        print("hello",username,    password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"logined successfully")
            return redirect('home')
        else:
            messages.error(request,"username or password is incorrect")
            return redirect('login')
    return render(request,'registration/login.html')
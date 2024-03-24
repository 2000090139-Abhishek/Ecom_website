
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import socket
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Product


def home(request):
    product = Product.objects.all()  # Retrieve all Product objects from the database
    return render(request, 'home.html', {'product': product})
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 != password2:
            return render(request, 'Register.html', {'error': 'Passwords do not match'})
        
        # Validate password
        try:
            validate_password(password1)
        except ValidationError as e:
            return render(request, 'Register.html', {'error': ', '.join(e.messages)})

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'Register.html', {'error': 'Username is already taken'})
        if User.objects.filter(email=email).exists():
            return render(request, 'Register.html', {'error': 'Email is already taken'})

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1,
                                         first_name=first_name, last_name=last_name)
        user.save()

        return redirect('login')

    return render(request, 'Register.html')


# Create your views here.
def loginUser(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        # Validate password
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "Login.html", {'error': 'User or password is not correct!'})

    return render(request, "Login.html")







def logOutUser(request):
    logout(request)
    return redirect("home")

from math import prod
from urllib import request
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
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
from django.shortcuts import render, redirect
from .models import Product, CartItem
from .forms import CartItemForm



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

def product_details(request, pk):
    # Retrieve the product with the given primary key or return a 404 error if not found
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product,  # Pass the single product object to the template
    }

    return render(request, 'Pdetails.html', context)


@login_required
def cart_details(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Check if the product is already in the cart
            cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            return redirect('cart')
    else:
        form = CartItemForm()
    return render(request, 'cart.html', {'form': form, 'product': product})

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def save_for_later(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.save_for_later = True
    cart_item.save()
    return redirect('cart')

def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})


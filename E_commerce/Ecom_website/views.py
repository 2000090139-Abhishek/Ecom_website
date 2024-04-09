

import json
from django.http import JsonResponse
from django.urls import reverse

from math import prod
from urllib import request


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

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import *





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


# def cart(request):
#     if request.user.is_authenticated:
#         user = request.user
#         if hasattr(user, 'customer'):
#             customer = user.customer
#         else:
#             # Create a Customer object for the user if it doesn't exist
#             customer = Customer.objects.create(user=user, name=user.username, email=user.email)
        
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#         print(items)
#     else:
#         items = []

#     context = {'items': items}
#     return render(request, 'cart.html', context)

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        customer, created = Customer.objects.get_or_create(user=user, defaults={'name': user.username, 'email': user.email})
        
        
        orders = Order.objects.filter(customer=customer, complete=False)
        if orders.exists():
           order = orders.first()  
        else:
           order = Order.objects.create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        
    else:
        items = []
        order={'get_cart_total':0, 'get_cart_items':0, 'shipping':False}

    context = {'items': items,'order':order}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        customer, created = Customer.objects.get_or_create(user=user, defaults={'name': user.username, 'email': user.email})
        orders = Order.objects.filter(customer=customer, complete=False)
        if orders.exists():
           order = orders.first()  
        else:
           order = Order.objects.create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order={'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    context = {'items': items, 'order': order}
    return render(request, 'Checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
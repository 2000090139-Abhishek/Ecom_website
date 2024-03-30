from django.core.exceptions import ObjectDoesNotExist
from .models import CartItem, Cart
from math import prod
from urllib import request
import uuid
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

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import Product, CartItem,Cart
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


def _cart_id(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart_id = str(uuid.uuid4())  # Generate a unique cart ID
        request.session['cart_id'] = cart_id
    return cart_id



def cart_details(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        try:
          pass
        except:
            pass 

        try:
          cart_item = CartItem.objects.get(user=current_user,product=product)
          cart_item.quantity +=1
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
            product = product,
            quantity =1,
            user = current_user
        )
         
        cart_item.save()

        return redirect('cart')
    else:
        try:
          cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id= _cart_id(request)
            )  
            cart.save()  
        try:
           cart_item = CartItem.objects.get(cart=cart, product=product)
           cart_item.quantity +=1
           cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product =product,
                cart = cart,
                quantity = 1
            )
            cart_item.save()  
        return redirect('cart.html')      

 
def remove_cart(request, product_id):
    current_user = request.user
    if current_user.is_authenticated:
  
         product = get_object_or_404(Product, id=product_id)
         
         cart_item = CartItem.objects.get(product=product, user=current_user)
         if cart_item.quantity > 1:
               cart_item.quantity -=1
       
               cart_item.save()
         else:
           cart_item.delete()
         return redirect('cart.html')
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete() 
        return redirect('cart.html')  

def remove_cart_item(request, product_id):
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, user=current_user)
        cart_item.delete()   
   
        return redirect('cart.html')
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()  
        
        return redirect('cart.html')


def cart(request, total=0, quantity=0,cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user =request.user, is_active=True)
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
           cart_items = CartItem.objects.filter(cart=cart, is_active=True)
       
        for cart_item in cart_items:
            total +=(cart_item.product.price *cart_item.quantity)
            quantity += cart_item.quantity    
    except ObjectDoesNotExist:
        pass  

    context ={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }        
               
    return render(request, 'cart.html',context)




def checkout(request, total=0,quantity=0 ,cart_items=None,):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user =request.user, is_active=True)
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
           cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total +=(cart_item.product.price *cart_item.quantity)
            quantity += cart_item.quantity  
    except ObjectDoesNotExist:
        pass  

    context ={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }        
          
    
    return render(request, 'checkout.html',context)


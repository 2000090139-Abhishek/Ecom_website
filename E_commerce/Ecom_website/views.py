
from django.shortcuts import render,HttpResponse
from .models import Product
# Create your views here.

def home(request):
    prod1 = Product()
    prod1.name="Laptop"
    prod1.img = 'prod_mage_1.jpg'
    prod1.price=2000
    prod1.description = 'Laptop'
    prod1.offer = True
    product =[prod1]
    return render (request, 'home.html',{'product':product})
    
    
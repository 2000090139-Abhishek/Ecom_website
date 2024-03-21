
from django.shortcuts import render,HttpResponse
from .models import Product


def home(request):
    product = Product.objects.all()  # Retrieve all Product objects from the database
    return render(request, 'home.html', {'product': product})
    
    
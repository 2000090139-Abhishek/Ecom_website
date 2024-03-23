
from django.shortcuts import render,HttpResponse
from .models import Product


def home(request):
    product = Product.objects.all()  # Retrieve all Product objects from the database
    return render(request, 'home.html', {'product': product})
    
def auth(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user_data = {
            'name' : username,
            'pass' : password
        }
        return render(request, 'home.html', {'product': product})
    else:
        return render(request,'auth.html)

# Create your views here.
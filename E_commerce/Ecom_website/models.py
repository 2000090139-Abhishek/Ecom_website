from django.db import models
from psutil import users

class Product(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(blank=True,null=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Auth(models.Model):
    user = models.OneToOneField(users, on_delete=models.CASCADE, primary_key=True)
    phone = models.DecimalField(max_digits=13+ 1, decimal_places=0) # +1 for '+' sign
    address = models.CharField(max_length=300)


    def __str__(self):
        return f"{self.user}"  #return username or something else?
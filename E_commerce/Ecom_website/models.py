from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(blank=True,null=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Auth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.DecimalField(max_digits=13+ 1, decimal_places=0) # +1 for '+' sign
    address = models.CharField(max_length=300)


    def __str__(self):
        return f"{self.user}"
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    save_for_later = models.BooleanField(default=False)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.subtotal()})"

    class Meta:
        unique_together = ('user', 'product', 'save_for_later')

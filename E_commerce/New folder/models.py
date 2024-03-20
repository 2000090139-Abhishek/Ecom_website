from django.db import models

# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    offer = models.BooleanField(default=False)
    
    # def __str__(self):
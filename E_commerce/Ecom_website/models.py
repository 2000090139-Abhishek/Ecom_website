from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='product/')  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name
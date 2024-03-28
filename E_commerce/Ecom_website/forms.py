from django import forms
from .models import CartItem

class CartItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, label='Quantity')

    class Meta:
        model = CartItem
        fields = ['quantity', 'save_for_later']
        labels = {
            'save_for_later': 'Save for Later'
        }

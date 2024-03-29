import statistics
from django.urls import path
from django.conf import settings



from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.loginUser,name="login"),
    path('signup/',views.register,name="register"),
    path('logout/',views.logOutUser,name="logout"),
    path('product/<int:pk>/', views.product_details, name='product_details'),

    
    path('cart/', views.cart, name='cart'),  # Keep this for displaying the cart
    path('cart/add/<int:product_id>/', views.cart_details, name='add_to_cart'),  # Rename this for adding products
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout')

]
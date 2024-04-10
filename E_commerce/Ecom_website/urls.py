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

    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    # path('update_item/',views.updateItem, name="updateItem"),
    path('update_item/', views.updateItem, name='update_item'),


]
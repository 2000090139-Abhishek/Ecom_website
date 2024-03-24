import statistics
from django.urls import path
from django.conf import settings



from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.loginUser,name="login"),
    path('signup/',views.register,name="register"),
    path('logout/',views.logOutUser,name="logout"),

]
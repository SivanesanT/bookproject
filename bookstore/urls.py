from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home, name='home'),
    path('shopcart',views.shopingcart, name='shopcart'),
    path('newshopcart/<int:pk>',views.newshopcart,name='newshopcart'),
    path('orders',views.orders, name='orders'),
    path("details/<int:pk>" ,views.detials, name='details'),
    path("register" ,views.register, name='register'),
    path("login" ,views.login, name='login'),
    path('loginuser',views.loginuser,name='loginuser'),
    path('registeruser', views.registeruser, name='regi'),
    path('logout', views.userlogout ,name='logout'),
    path('remove/<int:pk>',views.remove,name='remove'),
    path('placeorder/<int:pk>',views.placeorder,name='placeorder'),
    path('userregi',views.usserregister,name='userregi'),



]
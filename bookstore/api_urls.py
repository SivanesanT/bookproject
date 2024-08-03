from django.urls import include, path
from .views import *

# api/
urlpatterns = [
    path('books/', Apibooks.as_view()),
    path('books/<int:pk>/', Apibooks.as_view()),
    path('carts/', ApiCarts.as_view()),
    path('carts/<int:pk>/', ApiCarts.as_view()),
]
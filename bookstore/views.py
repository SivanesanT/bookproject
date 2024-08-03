from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.utils import timezone

# api pakages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
# Create your views here.
def home(request):
    bookset = Book.objects.filter(available = '1').order_by('id')
    return render(request,'store/home.html',{'book':bookset})
    # return render(request,'store/home.html')

def shopingcart(request):
    if  request.user.is_authenticated:
        user = request.user
        carts =Cart.objects.filter(user=user, cart_available=1,Order_status=0).order_by('-id')
        if carts:
            total_price = sum(cart.price for cart in carts)
            return render(request,'store/shopingcart.html',{'cart':carts,'total':total_price})
        else:
            messages.warning(request,"Non of the carts are available...")
            return redirect('home')
    else:
        messages.warning(request," user is found please login or register")
        return redirect('home')
    


def orders(request):
    if  request.user.is_authenticated:
        user = request.user
        carts =Cart.objects.filter(user=user, cart_available=0, Order_status=1).order_by('-id')
        if carts:
            total_price = sum(cart.price for cart in carts)
            return render(request,'store/orders.html',{'cart':carts,'total':total_price})
        else:
            messages.warning(request,"Non of the Orders are available...")
            return redirect('home')
    else:
        messages.warning(request," user is found please login or register")
        return redirect('home')
    


def detials(request,pk):
    get_data = Book.objects.get(id=pk)
    if get_data:
       return render(request, 'store/details.html' , {'data': get_data} )
    
def newshopcart(request,pk):
    if  request.user.is_authenticated:
        user = request.user
        get_data = Book.objects.get(id=pk)
        if get_data:
            newcart = Cart.objects.create(user=user , book=get_data, price=get_data.price)
            if newcart:
                messages.success(request,"Cart is Added Succcessfully...")
                return redirect('shopcart')
    else:
        messages.warning(request,"If You Want to give in Cart Please LogedIn")
        return redirect('login')
def placeorder(request,pk):
    if  request.user.is_authenticated:
        user = request.user
        item=pk
        if Cart.objects.filter(user=user , Order_status='1').exists():

            if Cart.objects.filter(id=item,cart_available='1'):
                get_cart = Cart.objects.get(id=item)
                book_instance=get_cart.book

                if Book.objects.filter(id=book_instance.id,available='1'):
                    book_instance.available='0'
                    book_instance.save()
                    get_cart.cart_available = '0'
                    get_cart.Order_status = '1'
                    get_cart.ordered_date = timezone.now()
                    get_cart.save()
                    messages.success(request,"your Order is placed")
                    return redirect('orders')
                else:
                    messages.warning(request,"The Book is Not available to order")
                    return redirect('shopcart')
            else:
                messages.warning(request,"This cart is Not available to order")
                return redirect('shopcart')
            
        else:
            messages.success(request,"Give some Details to Order")
            return render(request,'store/userdetails.html',{'cartid':item}) 
           
def usserregister(request):
        if  request.user.is_authenticated:
            user = request.user
            address=request.POST['address']
            number=request.POST['number']
            userid=request.POST['userid']
            cartid=request.POST['cartid']
            detail=userdetails.objects.create(user=user,address=address,number=number)
            if detail:
                if Cart.objects.filter(id=cartid,cart_available='1'):
                    get_cart = Cart.objects.get(id=cartid)
                    book_instance=get_cart.book

                    if Book.objects.filter(id=book_instance.id,available='1'):
                        book_instance.available='0'
                        book_instance.save()
                        get_cart.cart_available = '0'
                        get_cart.Order_status = '1'
                        get_cart.ordered_date = timezone.now()
                        get_cart.save()
                        messages.success(request,"your Order is placed")
                        return redirect('orders')
                    else:
                        messages.warning(request,"The Book is Not available to order")
                        return redirect('shopcart')

                else:
                    messages.warning(request,"This cart is Not available to order")
                    return redirect('shopcart')
                    
def register(request):
    if not request.user.is_authenticated:
        return render(request,'store/register.html')    
    else:
        messages.warning(request,"Your are already logedIn")
        return redirect('home')
    
def login(request):
    if not request.user.is_authenticated:
        return render(request,'store/login.html')
    else:
        messages.warning(request,"Your are already logedIn")
        return redirect('home')
    

def loginuser(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request,"Successfully logedIn")
            return redirect('home')
        else:
            messages.warning(request,"Invalid Username or Password")
            return redirect('login')
    else:
        return redirect('login')

    # return render(request,'store/login.html')

def registeruser(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['pass']
        cpassword=request.POST['cpass']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.warning(request,"This user name is already created so use another username")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                messages.success(request,"Registration is successfully completed Please Login")
                return redirect('login')
        else:
            messages.warning(request,"password and confirm passwored are not matched")
            return redirect('register')
    else:
        return redirect('register')
def userlogout(request):
    logout(request)
    messages.success(request,"Your are now logouted")
    return redirect('home')
def remove(request,pk):
    del_cart=Cart.objects.get(id=pk)
    del_cart.delete()
    messages.warning(request,"Cart Removed Successfully")
    return redirect('shopcart')



# api view
class Apibooks(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            books = Book.objects.all()
            serializers = BookSerializer(books, many=True)
            return Response(serializers.data, status=status.HTTP_201_CREATED)    

class ApiCarts(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            cart = Cart.objects.get(pk=pk)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            carts = Cart.objects.all()
            serializers = CartSerializer(carts, many=True)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
    
    # def post(self, request):
    #     serializer = CartSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk):
    #     cart= Cart.objects.get(pk=pk)
    #     serializer = CartSerializer(cart, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         # we want to give all data to update the data with id.
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def patch(self,request,pk):
    #     cart = Cart.objects.get(pk=pk)
    #     serializer=CartSerializer(cart,data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         # we want to give that change characteristic only with id.
    #         return Response(serializer.data)
    #     return Response(serializer.errors)

    # def delete(self, request, pk):
    #     member = Cart.objects.get(pk=pk)
    #     member.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    



    


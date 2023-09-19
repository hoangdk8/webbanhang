from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
# Create your views here.
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        user_not_login = "hidden"
        user_login = "show"
        context = {'first_name': first_name,'last_name': last_name,'email': email,'user_not_login':user_not_login,'user_login':user_login}
    else:
        user_not_login = "show"
        user_login = "hidden"
        context = {'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/profile.html', context)
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, completed = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_not_login = "hidden"
        user_login = "show"
    else:
        items=[]
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub = False)
    context={'products':products,'categories':categories,'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/detail.html',context)
def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category=request.GET.get('category','')
    products = Product.objects.all()
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context ={'categories':categories,'products':products,'active_category':active_category}
    if request.user.is_authenticated:  # Kiểm tra xem người dùng có đăng nhập hay không
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, completed = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        context['user_not_login'] = "hidden"
        context['user_login'] = "show"
        context['cartItems'] = cartItems
    else:
        items=[]
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        context['user_not_login'] = "show"
        context['user_login'] = "hidden"
        context['cartItems'] = cartItems
    return render(request,'app/category.html',context)

def search(request):
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all()
    searched = request.POST.get("searched", "")
    keys = Product.objects.filter(name__contains=searched) if searched else products
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, completed = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_not_login = "hidden"
        user_login = "show"
    else:
        items=[]
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        user_not_login = "show"
        user_login = "hidden"
    context={'searched': searched,'keys': keys,'products': products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories': categories,}
    return render(request,'app/search.html',context)

def register(request):
    form = CreateUserForm()
    if request.method =="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context ={'form':form,'user_not_login': "hidden", 'user_login': "hidden",'cart_not_login':"hidden",'cart_items_not_login':"hidden"}
    return render(request,'app/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
       
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request,'user or password is not correct!')
            
    context ={'user_not_login': "hidden", 'user_login': "hidden",'cart_not_login':"hidden",'cart_items_not_login':"hidden"}
    return render(request,'app/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, completed = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_not_login = "hidden"
        user_login = "show"
    else:
        items=[]
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all()
    context={'categories':categories,'products': products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, completed = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_not_login = "hidden"
        user_login = "show"
    else:
        items=[]
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context={'categories':categories,'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, completed = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_not_login = "hidden"
        user_login = "show"     
    else:
        items=[]
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context={'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login,'categories':categories}
    return render(request,'app/checkout.html',context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, completed = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product) 
    if action == 'add':
        orderItem.quantity +=1
    elif action =='remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('added',safe=False)
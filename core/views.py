from django.shortcuts import render
from .models import Order,OrderItem,Product,ShippingAddress
from .forms import CheckOutForm
from django.http import JsonResponse
from django.views.generic import ListView,View,DetailView
import json
import datetime
from django.contrib import messages
from .utils import cookieCart,cartData,guestUser
from django.contrib.auth.models import User

# Create your views here.
class homeView(ListView):
    paginate_by = 1
    def get(self,*args,**kwargs):
        products = Product.objects.all()
        data = cartData(self.request)
        cart_items = data['cart_items']
        context ={
            'products' :products,
            'cart_items':cart_items,
        }
        return render(self.request,'index.html',context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    context ={
        'items':items,
        'order':order,
        'cart_items':cart_items
    }
    return render(request,'cart.html',context)

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    form = data['form']
    cart_items = data['cart_items']
    context ={
        'items':items,
        'order':order,
        'form':form,
        'cart_items':cart_items
    }
    return render(request,'checkout.html',context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    user = request.user
    #
    try:
        product = Product.objects.get(id=productId)
        order,created = Order.objects.get_or_create(user=user,is_ordered=False)
        items = order.orderitem_set.all()
        order_item,created = OrderItem.objects.get_or_create(order=order,product=product)
    #
        if action == 'add':
            order_item.quantity += 1
            messages.info(request,"This item was added")
        elif action == 'remove':
            order_item.quantity -= 1
            messages.info(request,"One item removed from cart")
        order_item.save()
        if order_item.quantity <= 0:
            order_item.delete()
            messages.info(request,"This item has been removed from your cart")
    except:
        pass

def orderProcess(request):
    data = json.loads(request.body)
    print(data)
    transition_id = datetime.datetime.now().timestamp()
    user = request.user
    if user.is_authenticated:
        try:
            order,created = Order.objects.get_or_create(user=user,is_ordered=False)
        except:
            messages.warning(request,"Something went wrong")
    else:
        user,order = guestUser(request,data)

    total = float(data['form']['total'])
    order.transition_id = transition_id
    if total == float(order.get_cart_total):
        order.is_ordered = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            user = user,
            order = order,
            country  = data['shipping']['country'],
            city  = data['shipping']['city'],
            zipcode  = data['shipping']['zipcode'],
            street_address  = data['shipping']['street_address'],
            house_address  = data['shipping']['house_address']
        )
        messages.info(request,"Your order was successfull")
    return JsonResponse("Order is processed..",safe=False)
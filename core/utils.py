from .models import *
import json
from .forms import CheckOutForm
from django.contrib.auth.models import User

#second
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    
    items = []
    order = {'get_cart_total':0,'get_cart_item':0,'shipping':False}
    cart_items = order['get_cart_item']
        
    for i in cart:
        try:
            cart_items += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_item'] += cart[i]['quantity']

            item = {
                'product' : {
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'discount_price':product.discount_price,
                    'gender':product.gender,
                    'category':product.category,
                    'label':product.label,
                    'imageUrl':product.imageUrl,
                    'slug':product.slug,
                    'description':product.description,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'items':items,'order':order,'cart_items':cart_items}

#this fucntion create first
def cartData(request):
    form = CheckOutForm()
    user = request.user
    if user.is_authenticated:
        order,created = Order.objects.get_or_create(user=user,is_ordered=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_item
    else:
        cookie_cart = cookieCart(request)
        items = cookie_cart['items']
        order = cookie_cart['order']
        cart_items = cookie_cart['cart_items']
    return {'items':items,'order':order,'cart_items':cart_items,'form':form}

#guest user (third)
def guestUser(request,data):
    name = data['form']['name']
    email = data['form']['email']

    cookie_cart = cookieCart(request)
    items = cookie_cart['items']

    user,created = User.objects.get_or_create(email=email)
    user.name = name
    user.save()

    order = Order.objects.create(
        user = user,
        is_ordered = False
    )

    for item in items:
        product = Product.objects.get(id = item['product']['id'])

        order_item = OrderItem.objects.create(
            product=product,
            user=user,
            quantity = item['quantity']
        )
    return user,order
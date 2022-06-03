import json

from django.http import JsonResponse
from django.shortcuts import render

from .models import *

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_quantity
    else:
        items = []
        order = {
            'get_quantity': 0,
            'get_shipping': 0,
            'get_cart_subtotal': 0,
            'get_cart_total': 0
        }
        cart_items = order['get_quantity']
    
    
    products = Product.objects.all()
    context = {
        'products': products,
        'cart_items': cart_items
    }
    return render(request, 'store/home.html', context)


def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_quantity
    else:
        items = []
        order = {
            'get_quantity': 0,
            'get_shipping': 0,
            'get_cart_subtotal': 0,
            'get_cart_total': 0
        }
    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_quantity
    else:
        items = []
        order = {
            'get_quantity': 0,
            'get_shipping': 0,
            'get_cart_subtotal': 0,
            'get_cart_total': 0
        }
        
    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items
    }
    return render(request, 'store/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,
                                                 complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order,
                                                         product=product)
    
    if action == 'remove':
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

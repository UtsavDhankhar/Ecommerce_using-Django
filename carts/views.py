from django.http import HttpResponse
from django.shortcuts import render , redirect
from store.models import Product
from .models import Cart , CartItem

# Create your views here.

def _cart_id(request):

    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    
    return cart


def add_cart(request , product_id):

    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))

    except Cart.DoesNotExist:

        cart = Cart.objects.create(
            cart_id = _cart_id(request),
        )
    
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product , cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )

        cart_item.save()

    return redirect('cart')



def remove_cart(request , product_id):
    
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = Product.objects.get(id = product_id)
    cart_item = CartItem.objects.get(cart = cart , product = product)

    if(cart_item.quantity > 1):
        cart_item.quantity -= 1
        cart_item.save()
    
    else:

        cart_item.delete()

    return redirect('cart')


def remove(request , product_id):

    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = Product.objects.get(id = product_id)
    cart_item = CartItem.objects.get(cart= cart , product = product)

    cart_item.delete()

    return redirect('cart')



def cart(request):

    cart = Cart.objects.get(cart_id = _cart_id(request))

    cart_items = CartItem.objects.filter(cart = cart)

    quantity = 0
    total_price = 0

    for item in cart_items:
        quantity += item.quantity
        total_price += item.product.price * item.quantity
    
    tax = (total_price*8)/100

    total_after_tax = total_price + tax


    page_dict = {
        'cart' : cart,
        'cart_items' : cart_items,
        'quantity' : quantity,
        'total_price' : total_price,
        'tax' : tax,
        'total_after_tax' : total_after_tax,
        'path' : request.path

    }

    return render(request , 'carts/cart.html' , page_dict)
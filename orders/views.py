from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from carts.models import Cart , CartItem , address
from .models import Order

# Create your views here.
# @login_required(login = 'login')
def place_order(request):
    
    current_user = request.user

    cart_item = CartItem.objects.filter(user = current_user)
    cart_count = cart_item.count()

    if(cart_count <= 0):
        return redirect ('store')

    if(request.method == 'POST'):
        pass

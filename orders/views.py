from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from carts.models import Cart , CartItem , address
from orders.forms import OrderForm
from .models import Order
import calendar
import datetime
 
# Create your views here.
# @login_required(login = 'login')
def place_order(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    total = 0
    quantity = 0

    if(cart_count <= 0):
        return redirect ('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = (2*total)/100
    grand_total = total + tax


    if(request.method == 'POST'):
        print("in post")
        
        form = OrderForm(request.POST)
        print(form.is_valid)


        if form.is_valid():
            data = Order()
            data.address = form.cleaned_data['address']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.user = request.user
            data.save()

            #using data id and unix timestamp to generate unique order id
            date = datetime.datetime.utcnow()
            utc_time = calendar.timegm(date.utctimetuple())
            order_number = str(utc_time) + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user = current_user , is_ordered = False , order_number = order_number)
            
            page_dict = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'gtotal' : grand_total,
            }

            return render(request , 'orders/payment.html' , page_dict)
        
        else:
            return redirect('home')
        
    else:
        return redirect('home')


def payment(request):
    return render(request , 'orders/payment.html')
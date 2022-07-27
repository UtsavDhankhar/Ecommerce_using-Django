from django.shortcuts import get_object_or_404, render
from category.models import Category
from store.models import Product
from carts.models import Cart , CartItem
from carts.views import _cart_id

# Create your views here.

def store(request , category_slug = None):

    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category , slug = category_slug)
        products = Product.objects.all().filter(category=categories , is_available= True)

    else:
        products = Product.objects.all().filter(is_available = True)
    

    product_count = products.count()

    page_dict = {
        'products' : products,
        'product_count' : product_count
    }


    return render(request , 'store/store.html' , page_dict)





def product_detail(request , category_slug , product_slug):

    try:
        category_name = get_object_or_404(Category , slug = category_slug)
        product = get_object_or_404(Product , category=category_name , slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request) , product__slug = product_slug).exists()
    except Exception as e:
        raise e

    page_dict = {
        'product' : product,
        'in_cart' : in_cart
    }
    
    return render(request , 'store/product_detail.html' , page_dict)
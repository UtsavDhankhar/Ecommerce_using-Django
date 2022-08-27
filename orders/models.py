from django.db import models
from accounts.models import Account
from carts.models import address
from store.models import Product , Variation

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(Account , on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New' , 'New'),
        ('Accepted' , 'Accepted'),
        ('Completed' , 'Completed'),
        ('Cancelled' , 'Cancelled'),
    )

    user = models.ForeignKey(Account , on_delete=models.SET_NULL , null = True)
    payment = models.ForeignKey(Payment , on_delete=models.SET_NULL , blank = True , null = True)
    order_number = models.CharField(max_length=20)
    address = models.ForeignKey(address , on_delete=models.PROTECT)
    order_note = models.CharField(max_length=100 , blank = True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10 , choices = STATUS , default = "NEW")
    ip = models.CharField(max_length=20 , blank = True)
    is_ordered = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updaed_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.address.first_name + self.address.last_name

    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment , on_delete=models.SET_NULL , blank = True , null = True)
    usesr = models.ForeignKey(Account , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation , on_delete = models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length = 50)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.product.product_name
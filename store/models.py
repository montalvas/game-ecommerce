from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    score = models.PositiveIntegerField(null=True, default=0)
    image = models.ImageField(upload_to='covers', null=True, blank=True)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        
        return url
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    shipping = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Order: {self.id}'
    
    @property
    def get_quantity(self):
        orderitems = self.orderitem_set.all()
        if orderitems:
            quantity = orderitems.count()
        else:
            quantity = 0
        
        return quantity
    
    @property
    def get_cart_subtotal(self):
        orderitems = self.orderitem_set.all()
        if orderitems:
            total = sum([item.get_price for item in orderitems])
        else:
            total = 0
            
        return total
    
    @property
    def get_shipping(self):
        orderitems = self.orderitem_set.all()
        if orderitems:
            total_cart = sum([item.get_price for item in orderitems])
            if total_cart >= 250:
                total = 0
            else:
                total = sum([10 for item in orderitems])
        else:
            total = 0
            
        return total
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        if orderitems:
            shipping = sum([item.get_price for item in orderitems])
            if shipping >= 250:
                shipping = 0
            else:
                shipping = sum([10 for item in orderitems])
        
            subtotal = sum([item.get_price for item in orderitems])
            total = shipping + subtotal
        else:
            total = 0
            
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'OrderItem: {self.id}, product: {self.product}, order: {self.order}'
    
    @property
    def get_price(self):
        return self.product.price
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
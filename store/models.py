import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

class Sub_category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='ecommerce/brand-img', null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

LABEL = (
    ('N', 'New'),
    ('BS', 'Best Seller')
)

class Product(models.Model):
    Availability = (('In stock','In stock'),('Out of stock','Out of stock'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ecommerce/p-img')
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    availability = models.CharField(choices=Availability, null=True, max_length=100)
    label = models.CharField(choices=LABEL, max_length=2, null=True)
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("store:product", kwargs={
            "pk" : self.pk
        
        })

    def get_add_to_cart_url(self) :
        return reverse("store:add-to-cart", kwargs={
            "pk" : self.pk
        })

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coupons = models.ManyToManyField("store.Coupon",blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    saved = models.IntegerField(default=0)
    
    @property
    def total_cost(self):
        total_price = sum(cart_item.product.price for cart_item in self.cartitem_set.all())
        discount_amount = 0
        if self.coupons.all() is not None:
            for coupon in self.coupons.all():
                if coupon.type == 'Percentage':
                    discount_amount += total_price * coupon.discount / 100
                else:
                    discount_amount += coupon.discount

            grand_total = total_price - discount_amount
            return total_price, discount_amount, grand_total
        else:
            grand_total = total_price - discount_amount
            return total_price, discount_amount, grand_total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.product_qty * self.product.price

    def __str__(self):
        return self.product

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    active = models.BooleanField(default=False)
    type = models.CharField(max_length=100, default="Percentage")
    discount = models.IntegerField(default=100)
    date = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.coupon_code

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = PhoneNumberField(blank=True)
    pincode = models.CharField(max_length=150, null=False)
    address = models.CharField(max_length=250, null=False)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.address

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(null=False)
    discount_price = models.FloatField(default=0)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    order_status = (
        (1,'Pending'),
        (2,'Dispatched'),
        (3,'Out for delivery'),
        (4,'Delivered'),
        (5,'Cancel'),
        (6,'Return'),
    )
    status = models.IntegerField(choices=order_status, default=1)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)
    
    def serialize(self):
        return {
            'id': self.id,
            'status': self.status,
        }
    def grand_total(self):
        grand_total = 0
        grand_total = self.total_price - self.discount_price 
        return grand_total
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    
    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.products.name
    

import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from django.urls import reverse
from django.conf import settings


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    

class Order(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    # state = models.CharField(max_length=150, null=False)
    # county = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=False)
    orderstatus = (
        ('Cancelled','Cancelled'),
        ('Pending','Pending'),
        ('Our for delivery','Our for delivery'),
        ('Delivered','Delivered'),
    )
    status = models.CharField(max_length=150, choices=orderstatus, null=False)
    message = models.TextField(null=False)
    tracking_no = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)
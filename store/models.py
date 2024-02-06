import uuid
from django.db import models
from django.contrib.auth.models import User
from django import forms
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
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.name

import uuid
from django.db import models

from django.contrib.auth.models import User


from django import forms
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, null=False)
    trending = models.BooleanField(default=False, help_text='0=default, 1=Trending')
    
    def __str__(self):
        return self.name

class Sub_category(models.Model):
    name = models.CharField(max_length=255, null=False)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    brand = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='images/products')
    description = models.TextField(max_length=500, null=False)
    status = models.BooleanField(default=False, help_text='0=default, 1=Hidden')
    trending = models.BooleanField(default=False, help_text='0=default, 1=Trending')
    
    def __str__(self):
        return self.name

class Product_variant(models.Model):
    name = models.CharField(max_length=255, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, null=False)
    price = models.DecimalField(decimal_places=2,max_digits=5,null=False)
    mrp = models.DecimalField(decimal_places=2,max_digits=5,null=False)
    qty = models.IntegerField(null=False, blank=False)
    color = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
        
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

# class variation(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     name = models.CharField(max_length=150, null=False, blank=False)

#     def __str__(self):
#         return self.name

# class variation_option(models.Model):
#     variation = models.ForeignKey(variation, on_delete=models.CASCADE)
#     value = models.CharField(max_length=150, null=False, blank=False)

#     def __str__(self):
#         return self.value

# class user(models.Model):
#     name = models.CharField(max_length=150, null=False, blank=False)
#     email = models.EmailField(max_length=150, null=False, blank=False)
#     phone = models.IntegerField(null=False, blank=False)
#     password = models.CharField(max_length=150, null=False, blank=False)

#     def __str__(self):
#         return self.name

# class wishlist(models.Model):
#     product_item = models.ForeignKey(product_item, on_delete=models.CASCADE)
#     user = models.ForeignKey(user, on_delete=models.CASCADE)

# class state(models.Model):
#     state_name = models.CharField(max_length=150, null=False, blank=False)

#     def __str__(self):
#         return self.state_name

# class address(models.Model):
#     name = models.CharField(max_length=150, null=False, blank=False)
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('N', 'Not to say'),
#     )
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#     house_no = models.CharField(max_length=50, null=False, blank=False)
#     area = models.CharField(max_length=50, null=False, blank=False)
#     city = models.CharField(max_length=50, null=False, blank=False)
#     landmark = models.CharField(max_length=50, null=False, blank=False)
#     postalcode = models.IntegerField(null=False, blank=False)
#     ADDRESS_CHOICES = (
#         ('HOME', 'Home'),
#         ('WORK', 'Work'),
#     )
#     address_type = models.CharField(max_length=4, choices=ADDRESS_CHOICES)
#     mobile_no = models.IntegerField(null=False, blank=False)
#     alternate_no = models.IntegerField(null=False, blank=False)
#     is_default = models.BooleanField(default=False)
#     user = models.ForeignKey(user, on_delete=models.CASCADE)
#     state = models.ForeignKey(state, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.name
 

# class payment(models.Model):
#     value = models.CharField(max_length=20, null=False, blank=False)

#     def __str__(self):
#         return self.value
    
# class user_payment_method(models.Model):
#     user = models.ForeignKey(user, on_delete=models.CASCADE)
#     payment = models.ForeignKey(payment, on_delete=models.CASCADE)
#     provider = models.CharField(max_length=50, null=False, blank=False)
#     account_no = models.CharField(max_length=50, null=False, blank=False)
#     expiry_date = models.CharField(max_length=10, null=False, blank=False)
#     is_default = models.BooleanField(default=False)
    
# class order(models.Model):
#     product = models.ForeignKey(product_item, on_delete=models.CASCADE)
#     qty = models.IntegerField(null=False, blank=False)
#     price = models.IntegerField(null=False, blank=False)

# class review_img(models.Model):
#     img = upload_to='reviews' 
#     order = models.ForeignKey(order, on_delete=models.CASCADE)


# class user_review(models.Model):
#     user = models.ForeignKey(user, on_delete=models.CASCADE)
#     ordered_product_item = models.ForeignKey(order, on_delete=models.CASCADE)
#     rating = models.CharField(max_length=5, null=False, blank=False)
#     comment = models.TextField(null=False, blank=False)
#     image = models.ForeignKey(review_img, on_delete=models.CASCADE)

# class checkout(models.Model):
#     user = models.ForeignKey(user, on_delete=models.CASCADE)
#     payment = models.ForeignKey(user_payment_method, on_delete=models.CASCADE)
#     order = models.ForeignKey(order, on_delete=models.CASCADE)
#     order_date = models.DateTimeField(auto_now=True)
#     shipping_address = models.ForeignKey(address, on_delete=models.CASCADE)
#     order_total = models.FloatField()
#     ORDER_STATUS = (
#         ('SHIPPED', 'Shipped'),
#         ('DELIVERED', 'Delivered'),
#         ('ORDERED', 'Ordered'),
#     )
#     order_status = models.CharField(max_length=15, choices=ORDER_STATUS)

# class promotion(models.Model):
#     checkout = models.ForeignKey(checkout, on_delete=models.CASCADE)
#     name = models.CharField(max_length=150, null=False, blank=False)
#     description = models.TextField(null=False, blank=False)
#     discount_amt = models.FloatField(null=False, blank=False)
#     start_date = models.DateField(null=False, blank=False)
#     end_date = models.DateField(null=False, blank=False)


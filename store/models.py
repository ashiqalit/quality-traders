import uuid
import datetime
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from PIL import Image

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

class Offer(models.Model):
    name = models.CharField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Sub_category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='ecommerce/brand-img', null=True, blank=True)
    description = models.TextField(null=True)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

LABEL = (
    ('N', 'New'),
    ('BS', 'Best Seller'),
    ('O', 'Ordinary'),
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
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    total_offer = models.IntegerField(default=0)
    final_price = models.IntegerField(default=0)

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
        
    def get_discounted_price(self):
        product_discount = 0
        subcategory_discount = 0
        total_offer_price = 0

        if self.offer and self.offer.is_active:  # Check if there's a direct offer for the product
            product_discount = self.offer.discount

        # Check if there's an offer associated with the subcategory
        if self.sub_category.offer and self.sub_category.offer.is_active:
            subcategory_discount = self.sub_category.offer.discount
        
        # if product_discount < subcategory_discount:
        #     total_offer_price = product_discount
        # elif subcategory_discount < product_discount:
        #     total_offer_price = subcategory_discount
        # elif product_discount == subcategory_discount:
        #     total_offer_price = product_discount
        # total_offer_price = product_discount + subcategory_discount
        # Calculate the final discounted price by applying both discounts
        # discounted_price = self.price
        # if product_discount > 0 and product_discount < subcategory_discount:
        #     discounted_price -= (self.price * product_discount / 100)
        # elif subcategory_discount > 0 and subcategory_discount < product_discount:
        #     discounted_price -= (self.price * subcategory_discount / 100)
        # elif subcategory_discount > 0 and subcategory_discount > 0 and subcategory_discount == product_discount:
        #     discounted_price -= (self.price * subcategory_discount / 100)

        total_offer_price = max(product_discount, subcategory_discount)
        discounted_price = self.price - (self.price * total_offer_price / 100)
        return discounted_price, total_offer_price #percentage
    
    def get_discounted_offer(self):
        _,total_offer_price = self.get_discounted_price()
        offer_amount = self.price * total_offer_price / 100
        return offer_amount

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coupons = models.ManyToManyField("store.Coupon",blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    saved = models.IntegerField(default=0)
    
    @property
    def total_cost(self):
        total_price = round(float(sum(cart_item.product.price * cart_item.product_qty for cart_item in self.cartitem_set.all())),2)
        discount_amount = 0.0
        total_offer = 0
        sum_of_discount_price = 0
        for cart_item in self.cartitem_set.all():
            if cart_item.product.offer or cart_item.product.sub_category.offer: #checking if the product has product offer or subcategory offer
                
                discount_price,total_offer_price = cart_item.product.get_discounted_price() #fetching the discouted total price from product model
                #& fetching the discouted total price from product model
                total_offer += (cart_item.product.price * total_offer_price / 100) * cart_item.product_qty
                sum_of_discount_price += discount_price #adding each product's discounted price to get the total
        grand_total = sum_of_discount_price

        if self.coupons.all() is not None:
            for coupon in self.coupons.all():
                if coupon.type == 'Percentage':
                    discount_amount += total_price * coupon.discount / 100
                else:
                    discount_amount += coupon.discount

        grand_total -= discount_amount
            
        return total_price, discount_amount, grand_total, total_offer

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.PositiveIntegerField(default=1)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)  # Add this field to store discounted price
    
    def save(self, *args, **kwargs):
        # Calculate and store discounted price when saving cart item
        _,total_offer_price = self.product.get_discounted_price()
        self.discounted_price = total_offer_price * self.product_qty
        super().save(*args, **kwargs)

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
    coupon_discount_price = models.FloatField(default=0)
    offer_discount_price = models.FloatField(default=0)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    order_status = (
        (1,'Pending'),
        (2,'Dispatched'),
        (3,'Out for delivery'),
        (4,'Delivered'),
        (5,'Cancel'),
        (6,'Return'),
        (7,'Not Returnable'),
    )
    status = models.IntegerField(choices=order_status, default=1)
    payment_status = (
        (1,'Pending'),
        (2,'Success'),
        (3,'Failed'),
    )
    payment = models.IntegerField(choices=payment_status, default=1)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = PhoneNumberField(blank=True)
    pincode = models.CharField(max_length=150, null=False)
    address = models.CharField(max_length=250, null=False) 

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)
    
    def serialize(self):
        return {
            'id': self.id,
            'status': self.status,
        }
    @property
    def grand_total(self):
        grand_total = 0
        grand_total = round(Decimal(self.total_price - self.coupon_discount_price - self.offer_discount_price),2) 
        return grand_total
    
    @property
    def total_discount(self):
        total_discount = 0
        total_discount = self.coupon_discount_price + self.offer_discount_price
        return total_discount
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    
    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)

# order return
class ReturnRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_status = (
        (1,'Pending'),
        (2,'Approved'),
        (3,'Rejected'),  
    )
    status = models.CharField(choices=request_status, default=1, max_length=20)
    rejection_message = models.CharField(max_length=100, null=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.order.id, self.order.tracking_no, self.user.username)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.products.name
    

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # status = models.CharField(max_length=50, blank=True)
    # amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # is_credit = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}"
    
    @property
    def total(self):
        return self.wallettransaction_set.filter(wallet_id=self.id).aggregate(total_amount=Sum('amount'))['total_amount'] or 0.00
    
    def update_total(self, amount):
        current_total = self.total
        new_total = current_total + amount
        # self.wallettransaction_set.create(amount=amount, order=order, status='Wallet deduction', is_credit=amount>0)
        self.save()
        return new_total

class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_credit = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.wallet.user} {self.amount} {self.is_credit}"
    
class Banner(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    sub_title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    button_text = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to='ecommerce/banner_img')
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} {self.sub_title} {self.description}"
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     original_width, original_height = img.size
    #     aspect_ratio = original_width / original_height
    #     new_height = 400
    #     new_width = int(new_height * aspect_ratio)
    #     output_size = (new_width, new_height)
    #     img.thumbnail(output_size)
    #     img.save(self.image.path)
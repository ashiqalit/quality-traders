from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Product)
admin.site.register(Offer)
admin.site.register(Brand)
# admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Coupon)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(Wallet)
admin.site.register(WalletTransaction)
admin.site.register(Banner)
admin.site.register(ReturnRequest)

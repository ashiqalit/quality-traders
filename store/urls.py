from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('product/<str:id>', views.product_detail, name='product_detail'),

    # cart
    path('add-to-cart', views.add_to_cart, name='addtocart'),
    path('show-cart', views.show_cart, name='showcart'),
    # path('update-cart', views.update_cart, name='update_cart'),

    path('plus-cart', views.plus_cart, name='pluscart'),
    path('minus-cart', views.minus_cart, name='minuscart'),
    path('remove-cart', views.remove_cart, name='removecart'),
     
    # placeorder
    path('checkout', views.checkout, name='checkout'),
    path('view-order/<str:t_no>', views.view_order, name='orderview'),
    path('cancel-order', views.cancel_order, name='cancel-order'),
    path('return-order', views.return_order, name='return-order'),

    path('proceed-to-pay', views.razorpaycheck, name='proceed-to-pay'),
    # path('apply-coupon', views.apply_coupon, name='apply_coupon'),
    path('remove_coupon', views.remove_coupon, name='remove_coupon'),


]
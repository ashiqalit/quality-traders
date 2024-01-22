from django.urls import path
from . import views

from store.controller import cart

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.productview, name='product'),
    path('add-to-cart/', cart.addtocart, name='addtocart'),
    
]
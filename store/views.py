from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Category, Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse

# Create your views here.

@login_required(login_url="login")
def home(request):
    category = Category.objects.all()
    
    categoryId = request.GET.get('category')
    if categoryId:
        product = Product.objects.filter(sub_category = categoryId).order_by('-id')
    else:
        product = Product.objects.all()
    
    context = {
        'category':category,
        'product':product
    }
    return render(request, 'store/index.html', context)

def product_detail(request, id):
    category = Category.objects.all()
    product = Product.objects.filter(id = id).first()
    context = {
        'category':category,
        'product':product,
    }
    return render(request, 'store/product-details.html', context)

# cart


#checkout

def checkout(request):
    return HttpResponse('This is checkout')
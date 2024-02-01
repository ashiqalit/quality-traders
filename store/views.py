from django.shortcuts import render
from store.models import Category,Product,Product_variant, Sub_category
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login")
def home(request):
    category = Category.objects.all()
    product = Product.objects.all()
    variant = Product_variant.objects.all()
    context = {'category':category,
               'product':product,
               'variant':variant}
    return render(request, 'store/index.html', context)

@login_required(login_url="login")
def productview(request):
        context = {}
        return render(request,'store/product.html', context)


from django.shortcuts import render
from store.models import Category, Product
from django.contrib.auth.decorators import login_required
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



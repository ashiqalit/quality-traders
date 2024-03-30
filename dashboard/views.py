from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, admin
from django.contrib.auth.models import User, Group  
from store.models import Category, Product, Sub_category, Brand, Order, OrderItem
from django.contrib import auth
from .filters import UserFilter,CategoryFilter,ProductFilter, SubCategoryFilter, BrandFilter
from .forms import CategoryForm, ProductForm, SubCategoryForm, BrandForm, OrderForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
# from .forms import UserForm

# Create your views here.
@login_required(login_url="dashboard_login")
def dashboard(request):
    if 'username' not in request.session:
        return redirect('dashboard_login')    
    return render(request,'dashboard/other/index.html')

def adminLogin(request):
    if 'username' in request.session:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user_ = auth.authenticate(username=username, password=password)
            
        if user_ is not None:
            if not user_.is_superuser:
                messages.info(request, 'You do not have admin privileges')
                return redirect('dashboard_login')
            auth.login(request, user_)
            request.session['username'] = username
            return redirect('dashboard')       
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('dashboard_login')
    else:
        return render(request, 'dashboard/auth/admin_signin.html')

@login_required(login_url="dashboard_login")
def logout(request):
    if 'username' in request.session:
        request.session.flush()
    auth.logout(request)
    return redirect('dashboard_login')

# user............................................................
@login_required(login_url="dashboard_login")
def list_user(request):
    users = User.objects.all()
    _filter = UserFilter(request.GET, queryset=users)
    filtered_users = _filter.qs
    context = {'all_users':filtered_users}
    return render(request, 'dashboard/other/userlist.html', context)

@login_required(login_url="dashboard_login")
def update_user_status(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('userId')
            user = User.objects.get(id=user_id)
            ischecked = request.POST.get('ischecked') == 'true'  
            user.is_active = ischecked
            user.save()
            message = 'User activated' if ischecked else 'User blocked'
            return JsonResponse({'status': 'success', 'message': message})
        except User.DoesNotExist: 
            return JsonResponse({'status': 'error', 'message': 'Invalid user ID'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# categories.............................................................................
@login_required(login_url="dashboard_login")
def list_categories(request):
    categories = Category.objects.all()
    myFilter = CategoryFilter(request.GET, queryset=categories)
    filterd_categories = myFilter.qs
    context = {'all_categories' : filterd_categories, 'myFilter' : myFilter}
    return render(request, 'dashboard/other/categorylist.html', context)

@login_required(login_url="dashboard_login")
def create_categories(request):  
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_category')
        else:
            messages.info(request, 'Form invalid')
            return redirect('create_category')
    else:
        form = CategoryForm()
        return render(request, 'dashboard/other/addcategory.html', {'form':form})

@login_required(login_url="dashboard_login")
def update_category(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('read_categories')
    else:
        context = {
            'user' : category,
            'form' : form,
            'pk': category.pk,
        }    
        return render(request, 'dashboard/other/editcategory.html', context)

@login_required(login_url="dashboard_login")
def drop_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('categoryId')
        category = Category.objects.get(id=category_id)
        category.delete()
        return JsonResponse({'success':True})
        # return redirect('read_categories')
    return JsonResponse({'success':False})

# products.................................................................................
@login_required(login_url="dashboard_login")
def list_products(request):
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=products)
    filterd_products = myFilter.qs
    for product in products:
        product.availability = 'Out of stock' if product.quantity == 0 else 'In stock'
        product.save()
    context = {'all_products' : filterd_products, 'myFilter' : myFilter}
    return render(request, 'dashboard/other/productlist.html', context)

@login_required(login_url="dashboard_login")
def create_products(request):  
    # product - request.model.product
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('read_products')
        else:
            messages.info(request, 'Form invalid')
            return redirect('create_product')
    
    form = ProductForm()
    return render(request, 'dashboard/other/addproduct.html', {'form':form})

@login_required(login_url="dashboard_login")   
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('read_products')
    context = {'form':form,
               'pk': product.pk,}
    return render(request, 'dashboard/other/editproduct.html', context)

@login_required(login_url="dashboard_login")
def drop_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('productId')
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({'success':True})
        # return redirect('read_categories')
    return JsonResponse({'success':False})

# subcategories.............................................................
@login_required(login_url="dashboard_login")
def list_subcategories(request):
    subcategories = Sub_category.objects.all()
    myFilter = SubCategoryFilter(request.GET, queryset=subcategories)
    filterd_categories = myFilter.qs
    context = {'all_categories' : filterd_categories, 'myFilter' : myFilter}
    return render(request, 'dashboard/other/subcategorylist.html', context)

@login_required(login_url="dashboard_login")
def create_subcategories(request):  
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_subcategory')
        else:
            messages.info(request, 'Form invalid')
            return redirect('create_subcategory')
    else:
        form = SubCategoryForm()
        return render(request, 'dashboard/other/subaddcategory.html', {'form':form})

@login_required(login_url="dashboard_login")
def update_subcategory(request, pk):
    subcategory = Sub_category.objects.get(id=pk)
    form = SubCategoryForm(instance=subcategory)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('read_subcategories')
    else:
        context = {
            'user' : subcategory,
            'form' : form,
            'pk': subcategory.pk,
        }    
        return render(request, 'dashboard/other/editsubcategory.html', context)

@login_required(login_url="dashboard_login")
def drop_subcategory(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('subcategoryId')
        subcategory = Category.objects.get(id=subcategory_id)
        subcategory.delete()
        return JsonResponse({'success':True})
        # return redirect('read_categories')
    return JsonResponse({'success':False})

# brands.............................................................
@login_required(login_url="dashboard_login")
def list_brands(request):
    brands = Brand.objects.all()
    myFilter = BrandFilter(request.GET, queryset=brands)
    filterd_brands = myFilter.qs
    context = {'all_brands' : filterd_brands, 'myFilter' : myFilter}
    return render(request, 'dashboard/other/brandlist.html', context)

@login_required(login_url="dashboard_login")
def create_brands(request):  
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_brand')
        else:
            messages.info(request, 'Form invalid')
            return redirect('create_brand')
    else:
        form = BrandForm()
        return render(request, 'dashboard/other/addbrand.html', {'form':form})

@login_required(login_url="dashboard_login")
def update_brand(request, pk):
    brand = Brand.objects.get(id=pk)
    form = BrandForm(instance=brand)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('read_brands')
    else:
        context = {
            'user' : brand,
            'form' : form,
            'pk': brand.pk,
        }    
        return render(request, 'dashboard/other/editbrand.html', context)

@login_required(login_url="dashboard_login")
def drop_brand(request):
    if request.method == 'POST':
        brand_id = request.POST.get('brandId')
        brand = Brand.objects.get(id=brand_id)
        brand.delete()
        return JsonResponse({'success':True})
        # return redirect('read_categories')
    return JsonResponse({'success':False})

# orders...........................................................................
@login_required(login_url="dashboard_login")
def list_orders(request):
    orders = Order.objects.all()
    context = {'orders':orders}
    return render(request, 'dashboard/other/orderlist.html', context)

@login_required(login_url="dashboard_login")
def edit_order(request, pk):
    order = Order.objects.get(id=pk)
    # form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('read_orders')
        else:
            messages.info(request, 'Form invalid')
    else:
        form = OrderForm(instance=order)
    context = {
        'order':order,
        'form':form,
        'pk':order.pk,
    }
    return render(request, 'dashboard/other/editorder.html', context)

@login_required(login_url="dashboard_login")
def cancel_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.status = 5
        order.save()
        return JsonResponse({'success':True})
    return JsonResponse({'success':False})
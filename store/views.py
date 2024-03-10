from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Category, Product, Cart, Order, OrderItem, Address
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden
import random
from .forms import AddressForm


# Create your views here.

# @login_required(login_url="login")
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

# navbar
@login_required(login_url="login")
def navbar(request):
    user = request.user
    carts = Cart.objects.filter(user=user)
    cart_count = 0
    for cart in carts:
        cart_count += cart.product_qty
    context = {
        'cart_count':cart_count,
    }
    return render(request, 'store/includes/navbar.html',context)

# cart
@login_required(login_url="login")
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        qty = product.quantity
        cart = Cart.objects.filter(user=user,product_id=product_id)
        
        if not cart:
            if product.quantity > 0:
                    try:
                        Cart(user=user, product=product).save()
                        response_data = {'success': True, 'message': 'Product added to cart'}
                    except Product.DoesNotExist:
                        response_data = {'success': False, 'message': 'Product not found'}
                    except Exception as e:
                        response_data = {'success': False, 'message': 'Error adding product: ' + str(e)}
                    return JsonResponse(response_data)
            else:
                    response_data = {'success': False, 'message': 'Product out of stock'}
                    return JsonResponse(response_data)        
        
        else:
            cart = Cart.objects.get(user=user,product_id=product_id)
            product = Product.objects.get(id=product_id)
            qty = product.quantity

            if cart.product_qty < qty:
                cart.product_qty += 1
                # cart.product.quantity -= 1
                cart.save()
                response_data = {'success': True, 'message': 'Product added to cart'}
                return JsonResponse(response_data)
            else:
                response_data = {'success': False, 'message': "Only "+ str(qty) +" quantity available"}
                return JsonResponse(response_data)
        

    else:
        return HttpResponseForbidden('Invalid request method')

@login_required(login_url="login")
def show_cart(request):
    user = request.user
    carts = Cart.objects.filter(user=user)
   
    # Following code is to find the total cost in cart
    amount = 0.0
    for cart in carts:
        total_price = cart.product_qty * cart.product.price
        amount += total_price
        
    context = {
        'carts':carts,
        'amount':amount,
        }
    return render(request, 'store/cart_detail.html', context)


@login_required(login_url="login")
def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        product = Product.objects.get(id=product_id)
        qty = product.quantity
        cart = Cart.objects.get(product=product_id, user=request.user)
        if cart.product_qty < qty :
                
                cart.product_qty += 1
                # cart.product.quantity -= 1
                cart.save()

                amount = 0.0
                cart_count = 0
                cart_product = [p for p in Cart.objects.all() if p.user == request.user]
                for p in cart_product:
                    amt = (p.product_qty * p.product.price)
                    amount += amt
                    cart_count += p.product_qty
                data = {
                    'quantity':cart.product_qty,
                    'amount':amount,
                    'cart_count':cart_count,
                }
                return JsonResponse(data)
        

@login_required(login_url="login")
def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart = Cart.objects.get(product=product_id, user=request.user)

        cart.product_qty -= 1
        # cart.product.quantity += 1
        cart.save()

        amount = 0.0
        cart_count = 0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            amt = (p.product_qty * p.product.price)
            amount += amt
            cart_count += p.product_qty
        data = {
            'quantity':cart.product_qty,
            'amount':amount,
            'cart_count':cart_count,
        }
        return JsonResponse(data)

@login_required(login_url="login")
def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart = Cart.objects.get(product=product_id, user=request.user)
        cart.delete()

        amount = 0.0
        cart_count = 0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            amt = (p.product_qty * p.product.price)
            amount += amt
            cart_count += p.product_qty
        data = {
            'amount':amount,
            'cart_count':cart_count,
        }
        return JsonResponse(data)
# checkout
def checkout(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False) 
            address.user = request.user 
            address.save()
            messages.info(request, 'New address added')
            return redirect('checkout')
        selected_address_id = request.POST.get('selected_address')
        payment_mode = request.POST.get('payment_mode')
        if selected_address_id and payment_mode:
            selected_address = Address.objects.get(pk=selected_address_id)
            neworder = Order(user=request.user, payment_mode=payment_mode, address=selected_address)

            # cart's total price
            cartitems = Cart.objects.filter(user=request.user)
            total_price = 0
            for item in cartitems:
                total_price += item.product.price * item.product_qty
            neworder.total_price = total_price
            request.session['total_price'] = neworder.total_price

            # tracking number
            track_no = 'qt' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no = track_no) is None:
                track_no = 'qt' + str(random.randint(1111111, 9999999))
            neworder.tracking_no = track_no
            neworder.save()
            

            neworder_items = Cart.objects.filter(user = request.user)
            for item in neworder_items:
                OrderItem.objects.create(
                    order = neworder,
                    product = item.product,
                    price = item.product.price,
                    quantity = item.product_qty
            )
                orderproduct = Product.objects.filter(id=item.product.id).first() 
                orderproduct.quantity -= item.product_qty
                orderproduct.availability = 'Out of stock' if orderproduct.quantity == 0 else 'In stock'
                orderproduct.save()
               
            # clear the cart
            Cart.objects.filter(user=request.user).delete()

            messages.success(request, "Your order has been placed successfully")
            return redirect('/')
        else:
            messages.error(request, "Please select an address and payment method")
            return redirect('checkout')
            

       
    else:
        form = AddressForm()
        addresses = Address.objects.filter(user=request.user)
        cartitems = Cart.objects.filter(user=request.user)
        total_price = 0  
        for item in cartitems:
            total_price += item.product.price * item.product_qty
        context = {'form':form, 'addresses':addresses,'cartitems':cartitems, 'total_price':total_price}
        return render(request, "store/checkout.html", context)

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from store.models import Category, Brand, Product, Cart, CartItem, Order, OrderItem, Address, Coupon, Wishlist, WishlistItem, Wallet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
from .forms import AddressForm
from django.db import transaction
# from .filters import ProductFilter
from decimal import Decimal
# from .context_processors import filter_context
from django.template.loader import render_to_string


# Create your views here.

@login_required(login_url="login")
def home(request):
    category = Category.objects.all()
    brands = Brand.objects.all()

    products = Product.objects.all()
    
    # myFilter = ProductFilter(request.GET, queryset=products)
    # filterd_products = myFilter.qs

    context = {
        'category':category,
        'brands':brands,
        'products':products,

    }
    return render(request, 'store/index.html', context)

def filter_product(request):

    subcategories = request.GET.getlist('sub_category[]')
    brands = request.GET.getlist('brand[]')

    products = Product.objects.all()

    if len(subcategories) > 0:
        products = products.filter(sub_category__id__in=subcategories).distinct()
    
    if len(brands) > 0:
        products = products.filter(brand__id__in=brands).distinct()
    
    data = render_to_string('store/filteredproducts.html', {'products':products})
    return JsonResponse({"data":data})

@login_required(login_url="login")
def product_detail(request, id):
    category = Category.objects.all()
    product = Product.objects.filter(id = id).first()
    context = {
        'category':category,
        'product':product,
    }
    return render(request, 'store/product-details.html', context)

# cart
def update_cart_counter(cart): #count the cart_items
    all_cart_items = cart.cartitem_set.all()
    cart_counter = sum(item.product_qty for item in all_cart_items)
    return cart_counter

@login_required(login_url="login")
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id) #get the product
        qty = product.quantity


        try:
            cart = Cart.objects.get(user=user) #get existing cart
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user) #if not create new cart
        cart.save()
        wishlist_item = WishlistItem.objects.filter(products=product) #checks if the product exists in wishlist items table
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart) #get existing cart_item
            if cart_item.product_qty < qty: #if cart qty less the actual qty
                cart_item.product_qty += 1 #increment cart
                cart_item.save()
                cart_counter = update_cart_counter(cart)
                if wishlist_item.exists():  # Check if the product is in the wishlist
                    wishlist_item.delete()
                response_data = {'success': True, 'message': 'Product added to cart', 'cart_counter':cart_counter}
                return JsonResponse(response_data)
            else:
                cart_counter = update_cart_counter(cart)
                response_data = {'success': False, 'message': "Only "+ str(qty) +" quantity available", 'cart_counter':cart_counter}
                return JsonResponse(response_data)

        except CartItem.DoesNotExist:
            if qty > 0: #if not out of stock
                cart_item = CartItem.objects.create(
                    product = product,
                    product_qty = 1,
                    cart = cart
                )
                cart_counter = update_cart_counter(cart)
                if wishlist_item.exists():  # Check if the product is in the wishlist
                    wishlist_item.delete()
                response_data = {'success': True, 'message': 'Product added to cart', 'cart_counter':cart_counter}
                cart_item.save()
                return JsonResponse(response_data)
            else:
                cart_counter = update_cart_counter(cart)
                response_data = {'success': False, 'message': 'Product out of stock', 'cart_counter':cart_counter}
                return JsonResponse(response_data)
            

@login_required(login_url="login")
def show_cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user) 
    
    cart_items = []
    try:
        cart_items = cart.cartitem_set.all()
        total_offer_price = 0 
        for item in cart_items:
            total_offer_price += item.discounted_price
    except AttributeError:
        pass
    

    if request.method == 'POST':
        code = request.POST.get("code")
        print("Code:",code)
        cart = Cart.objects.get(user=request.user)

        if cart:
            coupon = Coupon.objects.filter(coupon_code__iexact=code, active=True).first()
            if coupon:
                for cart_coupon in cart.coupons.all():
                    if cart_coupon == coupon:
                        messages.warning(request, "Coupon already activated")
                        print("Coupon already activated")
                        return redirect('showcart') 
                cart.coupons.add(coupon)
                messages.success(request, "Coupon Activated")                
                return redirect('showcart')
            else:
                print("coupon does not exists")
                messages.warning(request, "Coupon does not exists")
                return redirect('showcart')

    total_price, discount_amount, _, total_offer= cart.total_cost

    discount_amount = Decimal(discount_amount)
    total_price = Decimal(total_price)
    total_offer = round(Decimal(total_offer),2)
    grand_total = total_price - total_offer - discount_amount

    context = {
        'cart':cart,
        'cart_items':cart_items,
        'grand_total': round(grand_total, 2),
        'total_price': total_price,
        'discount_amount': round(discount_amount, 2),
        'offer_discount': total_offer,
        }
    
    return render(request, 'store/cart_detail.html', context)

@login_required(login_url="login")
def remove_coupon(request):
    if request.method == 'POST': 
        cart = Cart.objects.get(user = request.user)
        # total_price, discount_amount, grand_total, _ = cart.total_cost
        coupon_id = request.POST.get('coupon_id')
        print(coupon_id)

        if cart and coupon_id:
            try:
                coupon = Coupon.objects.get(pk=coupon_id)
            except Coupon.DoesNotExist:
                messages.error(request, 'Coupon does not exist.')
                return redirect('showcart')

            cart.coupons.remove(coupon)
           
            cart.save()
            messages.success(request, 'Coupon removed successfully')
        else:
            messages.error(request, 'Invalid request')

        return redirect('showcart')
    

@login_required(login_url="login")
def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        product = Product.objects.get(id=product_id)
        qty = product.quantity
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.filter(product=product).first()
        
        if cart_items:
            if cart_items.product_qty < qty:
                cart_items.product_qty += 1
                cart_items.save()
                amount = 0.0
                cart_count = 0
                cart_product = [p for p in CartItem.objects.all() if p.cart.user == request.user]
                for p in cart_product:
                    amt = (p.product_qty * p.product.price)
                    amount += amt
                    cart_count += p.product_qty

                # total_offer_price = cart_items.discounted_price
                total_price, discount_amount, _, total_offer = cart.total_cost

                total_price = Decimal(total_price)
                total_offer = round(Decimal(total_offer),2)
                discount_amount = Decimal(discount_amount)
                grand_total = total_price - total_offer - discount_amount
                data = {
                    'success': True,
                    'quantity':cart_items.product_qty,
                    'amount':amount,
                    'offer_discount':total_offer,
                    'grand_total': round(grand_total, 2),
                    'cart_count':cart_count,
                    'coupon_discount': round(discount_amount, 2),
                }
                return JsonResponse(data)
            else:
                data = {'success': False, 'message': "Your limit reached"}
                return JsonResponse(data)
        
    else:
        return JsonResponse({'error': 'Invalid request method'})        

@login_required(login_url="login")
def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.filter(product=product).first()
        
        if cart_items:
                if cart_items.product_qty > 1:
                    
                    cart_items.product_qty -= 1
                    cart_items.save()

                    amount = 0.0
                    cart_count = 0
                    cart_product = [p for p in CartItem.objects.all() if p.cart.user == request.user]
                    for p in cart_product:
                        amt = (p.product_qty * p.product.price)
                        amount += amt
                        cart_count += p.product_qty
                    # total_offer_price = cart_items.discounted_price
                    # total_offer_price = cart_items.discounted_price
                    total_price, discount_amount, _, total_offer = cart.total_cost

                    total_price = Decimal(total_price)
                    total_offer = round(Decimal(total_offer),2)
                    discount_amount = Decimal(discount_amount)
                    grand_total = total_price - total_offer - discount_amount
                    data = {
                        'success': True,
                        'quantity':cart_items.product_qty,
                        'amount':amount,
                        'offer_discount':total_offer,
                        'grand_total': round(grand_total, 2),
                        'cart_count':cart_count,
                        'coupon_discount': round(discount_amount, 2),
                    }
                    return JsonResponse(data)
                else:
                    data = {'success': False, 'message': "Your limit reached"}
                    return JsonResponse(data)
        
    else:
        return JsonResponse({'error': 'Invalid request method'})        


@login_required(login_url="login")
def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(user=request.user)
        cart_item = cart.cartitem_set.filter(product=product).first()
        cart_item.delete()

        amount = 0.0
        cart_count = 0
        cart_product = [p for p in CartItem.objects.all() if p.cart.user == request.user]
        for p in cart_product:
            amt = (p.product_qty * p.product.price)
            amount += amt
            cart_count += p.product_qty
        _, _, _, total_offer = cart.total_cost
        
        data = {
            'amount':amount,
            'cart_count':cart_count,
            'offer_discount':total_offer,
        }
        return JsonResponse(data)

# checkout
@login_required(login_url="login")
def checkout(request):
    try:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user) 
        cart_items = cart.cartitem_set.all()

        total_offer_price = 0 
        for item in cart_items:
            total_offer_price += item.discounted_price #calculating offer applied price of all products in cart

        total_price, discount_amount, _, total_offer = cart.total_cost #fetching from model defenition total cost
        discount_amount = Decimal(discount_amount)
        total_price = Decimal(total_price)
        total_offer = round(Decimal(total_offer),2)
        grand_total = total_price - total_offer - discount_amount
    except CartItem.DoesNotExist:
        # If cart is empty, redirect to cart page
        return redirect('showcart')
    if not cart_items:
        # If cart items are empty, redirect to cart page
        return redirect('showcart')
    
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
        payment_id = request.POST.get('payment_id')
        
        if selected_address_id and payment_mode and cart_items:
            print('Payment method:',payment_mode)
            selected_address = Address.objects.get(pk=selected_address_id)
            neworder = Order(user=request.user, payment_mode=payment_mode, address=selected_address)
            neworder.total_price = total_price
            neworder.coupon_discount_price = discount_amount
            neworder.offer_discount_price = total_offer
            grand_total = neworder.grand_total
            # request.session['total_price'] = neworder.total_price

            # tracking number
            track_no = str(request.user.username) + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no = track_no) is None:
                track_no = 'qt' + str(random.randint(1111111, 9999999))
            neworder.tracking_no = track_no
            neworder.payment_id = payment_id
            neworder.save()
            

            neworder_items = cart_items
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
            for item in cart_items: item.delete()
            cart.delete()

            # payMode = request.POST.get('payment_mode')
            # if payMode == "Razorpay":
            #     return JsonResponse({'status':"Your order has been placed successfully"})
            # else:
            #     messages.success(request, "Your order has been placed successfully")
            #     return redirect('orderview', t_no=neworder.tracking_no)
            if payment_mode == "Razorpay":

                return JsonResponse({'status':"Your order has been placed successfully", 't_no':neworder.tracking_no})
            messages.success(request, "Your order has been placed successfully")
            return redirect('orderview', t_no=neworder.tracking_no)

        else:
            messages.error(request, "Please select an address or put items in to cart")
            return redirect('checkout')
        
    else:
        form = AddressForm()
        addresses = Address.objects.filter(user=request.user)
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        # total_price = 0  
        # for item in cart_items:
        #     total_price += item.product.price * item.product_qty
        
        context = {'form':form, 'addresses':addresses,'cartitems':cart_items, 'total_price':total_price, 'discount_amount':round(discount_amount, 2), 'offer_discount': total_offer, 'grand_total':round(grand_total, 2)}
        return render(request, "store/checkout.html", context)
    



@login_required(login_url='login')
def razorpaycheck(request):
    if request.method == 'GET':
        address_id = request.GET['address_id']
        if address_id is not None:    
            # print(address_id)
            address_ = Address.objects.filter(id=address_id, user=request.user).values().first()
            if address_:
                address_['phone'] = str(address_['phone'])
                cart = Cart.objects.get(user=request.user)
                total_price, discount_amount, grand_total, total_offer = cart.total_cost
                total_after_offer = total_price - total_offer - discount_amount
                # cart_items = cart.cartitem_set.all()
                # total_price = cart.total_cost
                # for item in cart_items:
                #     total_price = total_price + item.product.price * item.product_qty
                data = {'total_price': total_after_offer, 'address': address_}
                
                return JsonResponse(data)
            else:
                return JsonResponse({'error':'Address not found'}, status=404)
        else:
            return JsonResponse({'error':'Address Id missing'}, status=400)

@login_required(login_url="login")
def view_order(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    grand_total = order.grand_total
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order':order, 'orderitems':orderitems, 'grand_total':grand_total}
    return render(request, "store/order_view.html", context)

@login_required(login_url="login")
def cancel_order(request):
    if request.method == 'GET':
        try:
            order_id = request.GET['order_id']
            order = Order.objects.get(id=order_id, user=request.user)
            # Start transaction to ensure atomicity
            with transaction.atomic():
                # Change order status to 'Cancel'
                order.status = 5
                order.save()

                # Increment product quantities
                order_items = order.orderitem_set.all()
                for order_item in order_items:
                    product = order_item.product
                    product.quantity += order_item.quantity
                    product.save()
                
                wallet = Wallet.objects.create(
                    user = request.user,
                    order = order,
                    amount = order.grand_total,
                    status = 'Credited'
                )
                wallet.save()
            return JsonResponse({'message': 'Order Cancelled', 'order':order.serialize()})
        except Address.DoesNotExist:
            return JsonResponse({'error': 'Order does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url="login")
def return_order(request):
    if request.method == 'GET':
        try:
            order_id = request.GET['order_id']
            order = Order.objects.get(id=order_id, user=request.user)
            # Start transaction to ensure atomicity
            with transaction.atomic():
                # Change order status to 'Cancel'
                order.status = 5
                order.save()
    
                # Increment product quantities
                order_items = order.orderitem_set.all()
                for order_item in order_items:
                    product = order_item.product
                    product.quantity += order_item.quantity
                    product.save()
                
                wallet = Wallet.objects.create(
                    user = request.user,
                    order = order,
                    amount = order.grand_total,
                    status = 'Credited'
                )
                wallet.save()

            return JsonResponse({'message': 'Order will be picked by our staff', 'order':order.serialize()})
        except Address.DoesNotExist:
            return JsonResponse({'error': 'Order does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url="login")
def wishlist(request):
    try:
        wishlist = Wishlist.objects.get(user=request.user)
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(user=request.user) 

    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
    

    context = {
        "wishlist":wishlist,
        "wishlist_items":wishlist_items,
    }
    return render(request, "store/wishlist.html",context)

@login_required(login_url="login")
def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id = product_id)

        try:
            wishlist = Wishlist.objects.get(user = request.user)
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(user = request.user)

        try:
            wishlist_item = WishlistItem.objects.get(products=product, wishlist=wishlist)
            response_data = {'success': False, 'message': 'Product already in wishlist', 'wishlist_counter': wishlist.wishlistitem_set.count()}
        except WishlistItem.DoesNotExist:
            wishlist_item = WishlistItem.objects.create(products=product, wishlist=wishlist)
            response_data = {'success': True, 'message': 'Product added to wishlist', 'wishlist_counter': wishlist.wishlistitem_set.count()}
        
        return JsonResponse(response_data)

@login_required(login_url="login")
def remove_wishlistitem(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        print(product_id)
        product = Product.objects.get(id=product_id)
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_item = WishlistItem.objects.filter(products=product, wishlist=wishlist).first()
        wishlist_item.delete()
        wishlist_count = wishlist.wishlistitem_set.count()

        data = {
            'wishlist_count':wishlist_count
        }
        return JsonResponse(data)

@login_required(login_url="login")
def wallet(request):
    wallets = Wallet.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'wallets':wallets
    }
    return render(request, 'store/wallets.html', context)
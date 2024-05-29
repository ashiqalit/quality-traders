# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.cache import never_cache

# Local application
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from accounts.models import Profile
from store.forms import AddressForm
from store.models import (
    Address,
    Order,
    OrderItem,
    Cart,
    CartItem,
    Wallet,
    WalletTransaction,
)
# Create your views here.
=======
from django.contrib.auth.models import User, auth
from .forms import CreateUserForm
from django.http import JsonResponse, HttpResponse
from .models import Profile
import random, json, uuid
from .helper import MessageHandler

>>>>>>> origin/twilio


@never_cache
def registerpage(request):
    if request.user.is_authenticated:
<<<<<<< HEAD
        return redirect("home")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
=======
        return redirect('home')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            otp=random.randint(1000,9999)
            profile=Profile.objects.create(otp=f'{otp}')
            profile.uid = str(uuid.uuid4())
            if request.POST.get('method_otp')=="id_otp_1":
                messagehandler=MessageHandler(request.POST.get('phone'),otp).send_otp_via_whatsapp()
            else:
                pass
                # messagehandler=MessageHandler(request.POST.get('phone'),otp).send_otp_via_message()
            red=redirect(f'otp/{profile.uid}/')
            red.set_cookie("can_otp_enter",True,max_age=600) 
            return red  
    context = {'form':form}
    return render(request, 'store/auth/register.html', context)
>>>>>>> origin/twilio

                referred_code = form.cleaned_data["referred_code"]
                # checks if referral code entered
                if referred_code:
                    # if entered a code that does not exist with any user return an error
                    if not Profile.objects.filter(referral_code=referred_code).exists():
                        messages.error(request, "Referral code does not exists")
                        return redirect("register")
                    # if the entered referral code is correct then,
                    # form should be saved
                    # money should be added to the sender and reciever
                    else:
                        form.save()
                        messages.info(request, "User created successfully")
                        referred_user_profile = Profile.objects.filter(
                            referral_code=referred_code
                        ).first()
                        referred_user = referred_user_profile.user
                        try:
                            user_wallet = Wallet.objects.get(user=referred_user)
                        except:
                            user_wallet = Wallet.objects.create(user=referred_user)
                        WalletTransaction.objects.create(
                            wallet=user_wallet,
                            amount=50,
                            status="Referral bonus credited",
                        )
                        return redirect("login")
                # form can also be saved without a referral code
                else:
                    form.save()
                    messages.info(request, "User created successfully")
                    return redirect("login")
    context = {"form": form}
    return render(request, "registration/register.html", context)


@never_cache
def loginpage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password1")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Username or Password is incorrect")

    context = {"form": form}
    return render(request, "registration/login.html", context)


@login_required(login_url="login")
def logoutpage(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart.delete()
    except Cart.DoesNotExist:
        pass

    logout(request)
<<<<<<< HEAD
    return redirect("login")


# Profile
@login_required(login_url="login")
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("view_profile")
        else:
            messages.error(request, f"Enter valid input")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "store/user_profile.html", context)


# Address
@login_required(login_url="login")
def profile_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.info(request, "New address added")
            return redirect("profile_address")
    else:
        form = AddressForm()
    addresses = Address.objects.filter(user=request.user)
    address_count = addresses.count()
    # Applying pagination
    paginator = Paginator(addresses, 3)
    page = request.GET.get("page")
    try:
        addresses = paginator.page(page)
    except PageNotAnInteger:
        addresses = paginator.page(1)
    except EmptyPage:
        addresses = paginator.page(paginator.num_pages)
    context = {"form": form, "addresses": addresses, "count": address_count}
    return render(request, "store/edit_address_profile.html", context)


@login_required(login_url="login")
def edit_address(request, pk):
    address = Address.objects.get(id=pk)
    form = AddressForm(instance=address)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect("profile_address")
    context = {
        "form": form,
        "pk": address.pk,
    }
    return render(request, "store/edit_address.html", context)


@login_required(login_url="login")
def remove_address(request):
    if request.method == "GET":
        try:
            address_id = request.GET["address_id"]
            address = Address.objects.get(id=address_id, user=request.user)
            address.delete()
            address_count = Address.objects.filter(user=request.user).count()

            return JsonResponse(
                {
                    "message": "Address deleted successfully",
                    "address_count": address_count,
                }
            )
        except Address.DoesNotExist:
            return JsonResponse({"error": "Address does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# Orders
@login_required(login_url="login")
def profile_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    # Applying pagination
    paginator = Paginator(orders, 10)
    page = request.GET.get("page")
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context = {
        "orders": orders,
    }
    return render(request, "store/edit_orders_profile.html", context)
=======
    messages.success(request, 'Logged out Successfully')
    return redirect('login')

def otpVerify(request,uid):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        profile=Profile.objects.get(uid=uid)     
        if request.COOKIES.get('can_otp_enter')!=None:
            if request.POST['otp'] == profile.otp:
                red=redirect('home')
                red.set_cookie('verified',True)
                return red
    return render(request,"store/auth/otp.html",{'id':uid})
  
     
>>>>>>> origin/twilio

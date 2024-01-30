from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .forms import CreateUserForm
from django.http import JsonResponse, HttpResponse
from .models import Profile
import random, json, uuid
from .helper import MessageHandler



def registerpage(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
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

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'success':True})
        else:
            # messages.info(request, 'Username or Password incorrect')
            return JsonResponse({'success':False, 'error':'Invalid Credentials'})
    context={}
    return render(request, 'store/auth/login.html', context)

@login_required(login_url='login')
def logoutpage(request):
    logout(request)
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
  
     
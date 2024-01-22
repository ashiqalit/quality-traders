from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .forms import CreateUserForm
from django.http import JsonResponse


def registerpage(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
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
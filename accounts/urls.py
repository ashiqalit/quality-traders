from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registerpage, name='register'),
    path('login', views.loginpage, name='login'),
    path('logout', views.logoutpage, name='logout'),    

]

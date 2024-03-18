from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='ecommerce/profile_pic/default.png', upload_to="ecommerce/profile_pic")
    phone = PhoneNumberField(blank=True)
    Gender = (('Male','Male'),('Female','Female'))
    gender = models.CharField(choices=Gender, null=True, max_length=10)
    date_of_birth  = models.DateField(null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
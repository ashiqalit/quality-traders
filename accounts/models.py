from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# Create your models here.

class Catagory(models.Model):
    name = models.CharField(max_length=150)

class Sub_Category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE)
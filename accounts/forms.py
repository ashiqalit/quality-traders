
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.forms import ModelForm, ChoiceField
from django import forms

CHOICES = [('1', 'SMS'), ('2', 'Whatsapp'),]

class CreateUserForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name','id':'first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name','id':'last_name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username','id':'username'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Phone Number', 'name':'phone_number','id':'phone'}))
    otp = forms.ChoiceField(widget=forms.RadioSelect(attrs={'name': 'otp','id':'otp'}),choices=CHOICES)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email','id':'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password','id':'password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','id':'password2'}))

    class Meta:
        model = Profile
        fields = ('first_name','last_name','username','phone','otp','email','password1','password2')



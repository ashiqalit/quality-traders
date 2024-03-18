from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Address


class AddressForm(forms.ModelForm):
    fname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Firstname', 'style': 'width: 200px;'}), label='First Name')
    lname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Lastname', 'style': 'width: 200px;'}), label='Last Name')
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email', 'style': 'width: 200px;'}))
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number', 'style': 'width: 200px;'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Pincode', 'style': 'width: 200px;'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Address', 'style': 'width: 200px;'}))
    class Meta:
        model = Address
        fields = ('fname','lname','email','phone','pincode','address')




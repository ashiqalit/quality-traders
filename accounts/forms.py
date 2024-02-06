
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}),error_messages={'exists':'Email already exists'})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    is_active = forms.BooleanField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']    

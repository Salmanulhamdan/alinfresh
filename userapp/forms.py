from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Address

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone_number', 'password',]



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')

class AddressForm(forms.ModelForm):
    class Meta:
        model= Address
        fields=['name','house','place', 'address_line', 'ultranate_phone']

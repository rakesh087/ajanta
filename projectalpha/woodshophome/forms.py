from django import forms
from django.forms import ModelForm
from .models import Account, Order
from django.contrib.auth.forms import UserCreationForm


class ForgotPassword(forms.Form):
    username=forms.CharField(label='Username')
    mobile_number=forms.IntegerField(help_text='Enter your registered mobile number', label='Mobile number')

class CapturePassword(forms.Form):
    password1=forms.CharField(min_length=8,label="New Password", widget=forms.PasswordInput)
    password2=forms.CharField(min_length=8,label="Confirm new Password", widget=forms.PasswordInput)

class Register(UserCreationForm):
    class Meta:
        model=Account
        fields=['email','username','mobile_number']

#this form will be for getting order from customers
class GetOrder(ModelForm):
    class Meta:
        model=Order
        fields=['order_item','order_unit','order_desc']

#this class is for renderring form for checking order status
class OrderStatus(forms.Form):
    order_number=forms.CharField(label='Order number')
    order_status=forms.CharField(label='Order Status')
    ordered_date=forms.DateField()
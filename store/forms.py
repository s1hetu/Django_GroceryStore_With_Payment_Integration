from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from . models import Customer, Brand
from django.core.exceptions import ValidationError


class ProfileUpdateFormUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['age', 'mobile_no', 'image']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerRegister(ModelForm):
    class Meta:
        model = Customer
        fields = ['mobile_no', 'age', 'gender']


class BrandRegister(ModelForm):
    class Meta:
        model = Brand
        fields = ['brand']














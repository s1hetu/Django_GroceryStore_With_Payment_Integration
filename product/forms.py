from django import forms

from constants import ORDER_UPDATE_STATUS_CHOICES
from .models import Order


class UpdateStatus(forms.ModelForm):
    status = forms.CharField(max_length=30, choices=ORDER_UPDATE_STATUS_CHOICES, default="Initialized")

    class Meta:
        model = Order
        fields = ['status']

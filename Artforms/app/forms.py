from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "username..."}),
            "email": forms.TextInput(attrs={"placeholder": "email..."}),
            "password1": forms.PasswordInput(attrs={"placeholder": "password..."}),
            "password2": forms.PasswordInput(
                attrs={"placeholder": "confirm password..."}
            ),
        }


class LoginUserForm(forms.Form):
    username = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "username..."})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "password..."})
    )


class CreateShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ["title", "description", "turnover", "base_price"]


class CreateRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ["contact_email", "description"]

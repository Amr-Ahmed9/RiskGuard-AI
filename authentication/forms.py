from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login, logout
from django import forms
from django.contrib.auth.password_validation import password_validators_help_text_html
from .models import UserProfile

class CreatUserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Last Name'
        })
    )

    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Email Address'
        })
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Username'
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Password'
        }),
          help_text=password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Repeat Password'
        })
    )

    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'custom-checkbox small inline-block'
        }),
        label="Are you using this for personal finance or business?",
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'user_type']
  




class LoginForm(forms.Form):
    
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Enter User Name...'
        })
    )

    password =forms.CharField(
        required = True,
        widget= forms.PasswordInput(attrs={
            'class':'form-control form-control-user',
            'placeholder':'Password'
        })

    )  
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
    required=True,
    widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Enter Email Address...'
        })
    )
    
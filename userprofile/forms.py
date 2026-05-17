from .models import UserProfile
from django import forms
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_type', 'email', 'phone', 'city', 'date_of_birth', 'profile_image']
        widgets = {
            'profile_type': forms.Select(attrs={'class': 'form-control' , 'placeholder': 'Select profile type'}),
            'email': forms.EmailInput(attrs={'class': 'form-control' , 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Enter phone number'}),
            'city': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Enter city'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control' , 'placeholder': 'Enter date of birth'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control' , 'placeholder': 'Upload profile image'}),
        }
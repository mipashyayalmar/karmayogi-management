from django import forms
from .models import UserProfile
from teacher import models

class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'photo' ,'date_of_birth']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
           'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
           'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

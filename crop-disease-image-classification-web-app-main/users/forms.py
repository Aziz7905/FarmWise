from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FarmerProfile, FarmerPost
from .models import Comment

class UserRegisterForm(UserCreationForm):
    """Extended user registration form with email field"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Form for updating basic User info"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class FarmerProfileUpdateForm(forms.ModelForm):
    """Form for updating farmer-specific profile info"""

    class Meta:
        model = FarmerProfile
        fields = ['farm_name', 'location', 'crops_grown', 'contact_number', 'about', 'profile_image']

class FarmerPostForm(forms.ModelForm):
    """Form for creating a new post by a farmer"""

    class Meta:
        model = FarmerPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title...'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write something about your farm...'}),
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'})
        }

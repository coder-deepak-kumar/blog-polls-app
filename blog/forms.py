from django import forms
from .models import Post, Category, Tag, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('id','created_date','author','slug')

class RegistorForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "age", "mobile","user_img"]

class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "age", "mobile"]


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name", "desc",]


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ["name", "desc",]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
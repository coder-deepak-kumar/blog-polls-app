from django import forms
from .models import Post, Category, Tag, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('id','created_date','author','slug')

class RegistorForm(UserCreationForm):
    first_name = forms.CharField(max_length=50 , required=True) 
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField()
    mobile = forms.IntegerField(label='Mobile Number',validators=[MinValueValidator(0),
                                       MaxValueValidator(10)])

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name should contain only letters")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should contain only letters")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email address")
        return email
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "age", "mobile","user_img"]

class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "age", "mobile", "user_img"]


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
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, User, Category, Tag
from django.utils import timezone
from .forms import PostForm, RegistorForm, LoginForm, ProfileForm, CategoryForm, TagForm
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#Post
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


#Authentication
def register_view(request):
    if request.method == "POST":
        form = RegistorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    
    else:
        form = RegistorForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('post_list')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('post_list')

@login_required
def profile(request):
    user = request.user
    return render(request, 'auth/profile.html', {"user": user})

@login_required
def profile_edit(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User Details updated succesfully.')
            return redirect('user-profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'auth/profile_edit.html', {'form':form})

#Category
def new_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'New Category created succesfully.')
            return redirect('post_list')
    else:
        form = CategoryForm()
    return render(request, 'category/new_category.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})


#Tags
def new_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'New Category created succesfully.')
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'tag/new_tag.html', {'form': form})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag/tag_list.html', {'tags': tags})
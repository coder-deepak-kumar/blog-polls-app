from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag, Comment, User
from django.utils import timezone
from .forms import PostForm, RegistorForm, LoginForm, ProfileForm, CategoryForm, TagForm, CommentForm
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
import csv, os
from django.apps import apps


#Post
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', post.slug)
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
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

def user_posts(request, id):
    author = get_object_or_404(User, id=id)
    posts = Post.objects.filter(author=author)
    return render(request, 'blog/post_list.html', {'posts': posts})


#Category
@login_required
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

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/post_list.html', {'posts': posts})

#Tags
@login_required
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

def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tag=tag)
    return render(request, 'blog/post_list.html', {'posts': posts})


#Admin panel File Export
def export(request):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f'user_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, unique_filename)

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for model in apps.get_models():
            fields = [field.name for field in model._meta.fields]
            writer.writerow([f'{model.__name__}'])
            writer.writerow(fields)
            for instance in model.objects.all():
                writer.writerow([getattr(instance, field) for field in fields])
            writer.writerow([])  

    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user.csv"'

    return response
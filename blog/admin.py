from django.contrib import admin
from .models import Post, Category, Tag, Comment, User
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin
from import_export.admin import ExportActionMixin

@admin.register(User)
class UserAdmin(ExportActionMixin, OrigUserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email','age','mobile','user_img')
    list_filter = ('id', 'username', 'email')
    search_fields = ('id', 'username', 'email')


@admin.register(Comment)
class CommentAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'body', 'post', 'created', 'updated', 'active', 'parent')
    list_filter = ('id', 'email', 'active')
    search_fields = ('id', 'email', 'active',)
    autocomplete_fields = ['post','parent']

@admin.register(Post)
class PostAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'author', 'category', 'title', 'text', 'created_date', 'published_date', 'feature_img','thumbnail_img', 'slug')
    list_filter = ('id', 'author', 'category')
    search_fields = ('id', 'slug')    
    autocomplete_fields = ['author','category']
    filter_horizontal = ['tag']

@admin.register(Category)
class CategoryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'slug')
    list_filter = ('id', 'slug')
    search_fields = ('id', 'slug')

@admin.register(Tag)
class TagAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'slug')
    list_filter = ('id', 'slug')
    search_fields = ('id', 'slug')



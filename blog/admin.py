from django.contrib import admin
from .models import Post, Category, Tag, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin
from import_export.admin import ExportActionMixin

User = get_user_model()


@admin.register(User)
class UserAdmin(ExportActionMixin, OrigUserAdmin):
  list_display = (
    'id', 'first_name', 'last_name', 'username', 'email','age','mobile'
  )

@admin.register(Comment)
class CommentAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Post)
class PostAdmin(ExportActionMixin, admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(ExportActionMixin, admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(ExportActionMixin, admin.ModelAdmin):
    pass



from django.contrib import admin
from .models import Post, Category, Tag, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(OrigUserAdmin):
  list_display = (
    'id', 'first_name', 'last_name', 'username', 'email','age','mobile'
  )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')



admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
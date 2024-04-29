from django.contrib import admin
from .models import Post
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(OrigUserAdmin):
  list_display = (
    'id', 'first_name', 'last_name', 'username', 'email','age','mobile'
  )
admin.site.register(Post)
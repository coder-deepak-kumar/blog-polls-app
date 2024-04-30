from django.urls import path, include
from . import views

urlpatterns = [
    #Post
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name="post_detail"),
    path('post/new', views.post_new, name="post_new"),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

    #Authentication
    path('register', views.register_view, name="register_view"),
    path('login', views.login_view, name="login_view"),
    path('logout', views.logout_view, name="logout_view"),

    #Profile
    path('profile', views.profile, name='user-profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),

    #Category
    path('category/new', views.new_category, name="new_category"),
    path('categories', views.category_list, name="category_list"),

]

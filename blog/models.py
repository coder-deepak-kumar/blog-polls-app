from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from autoslug import AutoSlugField

class User(AbstractUser):
    age = models.IntegerField(default=18)
    mobile = models.CharField(max_length=10)
    
class Category(models.Model):
    name = models.CharField(max_length=60)
    desc = models.TextField()
    image = models.ImageField(upload_to='cat')
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=60)
    desc = models.TextField()
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    feature_img = models.ImageField(upload_to='image/feature_img/')
    thumbnail_img = models.ImageField(upload_to='image/thumbnail_img/')
    slug = AutoSlugField(populate_from='title', unique=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
    

class Comment(models.Model): 
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80) 
    email = models.EmailField() 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta: 
        ordering = ('created',) 

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post) 
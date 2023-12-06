from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

# Create your models here.
User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='s3://django-tutor-try/static/profile_post_images/blank-profile-picture.png')
    birthday = models.CharField(max_length=8, blank=True)
    
    def __str__(self):
        return self.user.username

    def delete(self):
        self.profileimg.delete()
        super().delete()
    
class Post(models.Model):
    id_post = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length = 100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    create_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)
    user_img = models.ImageField(upload_to='profile_post_images', default='s3://django-tutor-try/static/profile_post_images/blank-profile-picture.png')
    def __str__(self):
        return self.user
    
    def delete(self):
        self.image.delete()
        self.user_img.delete()
        super().delete()
    
class Like(models.Model):
    id_post = models.CharField(max_length=500)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
    def delete(self):
        super().delete()
    
class FollowerCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
    def delete(self):
        super().delete()
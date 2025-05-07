from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    crops_grown = models.CharField(max_length=255, blank=True)  
    contact_number = models.CharField(max_length=20, blank=True)
    about = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} (Farmer)'


class FarmerPost(models.Model):
    author = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f'{self.title} by {self.author.user.username}'

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(FarmerPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on "{self.post.title}"'

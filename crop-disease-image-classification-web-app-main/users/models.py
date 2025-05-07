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

class Fertilizer(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='fertilizers')
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)

class Pesticide(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='pesticides')
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)

class Material(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='materials')
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20, default='units')
    date = models.DateField(default=timezone.now)

class TreeType(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='trees')
    tree_name = models.CharField(max_length=100)
    count = models.PositiveIntegerField()

class CropField(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=5, decimal_places=2)
    stage = models.CharField(max_length=100)
    next_action = models.CharField(max_length=200)

class CropTask(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    date = models.DateField()

class Note(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

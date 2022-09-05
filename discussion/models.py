from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    user=models.ManyToManyField(User,related_name='subscribe',blank=True)
    def get_subscribe_url(self):
        return reverse('subscribe',args=[self.pk])
    
    
    def __str__(self) :
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    image=models.ImageField(upload_to='images')
    user=models.ForeignKey(User,related_name='postuser',on_delete=models.CASCADE)
    category=models.ForeignKey(Category,related_name='postcategory',on_delete=models.CASCADE)
    createdat=models.DateTimeField(auto_now_add=True)
    updatedat=models.DateTimeField(auto_now=True)
    like=models.ManyToManyField(User,related_name='likepost',blank=True)
    unlike=models.ManyToManyField(User,related_name='unlikepost',blank=True)
    def get_post_url(self):
        return reverse('post',args=[self.pk])
    def get_like_url(self):
        return reverse('likepost',args=[self.pk])
    def get_unlike_url(self):
        return reverse('unlikepost',args=[self.pk])
    def get_addcomment_url(self):
        return reverse('addcomment',args=[self.pk])
    
    def __str__(self) :
        return self.title
class Comment(models.Model):
    content=models.TextField()
    user=models.ForeignKey(User,related_name='commentuser',on_delete=models.CASCADE)
    post=models.ForeignKey(Post,related_name='commentpost',on_delete=models.CASCADE)
    createdat=models.DateTimeField(auto_now_add=True)
    updatedat=models.DateTimeField(auto_now=True)
    def get_addreply_url(self):
        return reverse('addreply',args=[self.pk])
    
        

class Reply(models.Model):
    content=models.TextField()
    user=models.ForeignKey(User,related_name='replyuser',on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,related_name='replycomment',on_delete=models.CASCADE)
    createdat=models.DateTimeField(auto_now_add=True)
    updatedat=models.DateTimeField(auto_now=True)
    
         
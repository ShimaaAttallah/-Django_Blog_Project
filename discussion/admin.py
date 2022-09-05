from django.contrib import admin

from discussion.models import Category, Comment, Post, Reply

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)

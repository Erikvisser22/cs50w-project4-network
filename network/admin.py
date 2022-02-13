import imp
from django.contrib import admin
from .models import Like, Post, Follower


# Register your models here.
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Follower)
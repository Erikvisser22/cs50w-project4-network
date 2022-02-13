from re import T
from statistics import mode
from tkinter.messagebox import NO
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    like_from_current_user = models.BooleanField(default=False)
    
    def __str__ (self):
        return f"{self.user} - Post {self.id}"

class Follower(models.Model):
    user = models.ForeignKey("User", default=None, related_name="user", on_delete=models.CASCADE)
    follower = models.ForeignKey("User", default=None, related_name="follower", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} - {self.user}"

class Like(models.Model):
    user = models.ForeignKey("User", default=None, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.post}"

    
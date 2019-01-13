from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PostLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

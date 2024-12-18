from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


# Create your models here.

class ForumThreads(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='forum_threads')

    def __str__(self):
        return self.title


class Comment(models.Model):
    thread = models.ForeignKey(ForumThreads, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.thread}"


class Like(models.Model):
    thread = models.ForeignKey(ForumThreads, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('thread', 'user')

    def __str__(self):
        return f"Like by {self.user} on {self.thread}"

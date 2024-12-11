from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from django.db import models

UserModel = get_user_model()


class Posts(models.Model):
    title = models.CharField(max_length=125)
    image = CloudinaryField('image')
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f"Post by {self.user.profile.get_display_name} at {self.created_at}"


class PostsComments(models.Model):
    post = models.ForeignKey(Posts, related_name='post_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


class PostLike(models.Model):
    post = models.ForeignKey(Posts, related_name='post_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"Like by {self.user} on {self.post}"

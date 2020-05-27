from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True
    )
    def get_connections(self):
        connections = UserConnection.objects.filter(follows_user=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(followed_user=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(followed_user=self)
        return followers.filter(follows_user=user).exists()

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def __str__(self):
        return self.username


class UserConnection(models.Model):
    follow_time = models.DateTimeField(auto_now_add=True, editable=False)
    follows_user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="follows")
    followed_user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="followed_by")
    class Meta:
        unique_together = ("follows_user", "followed_user")

    def __str__(self):
        return self.follows_user.username + ' follows ' + self.followed_user.username


class Post(models.Model):
    author = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='my_posts'
    )
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True
    )

    def get_absolute_url(self):
        return reverse("post_detail", args = [str(self.id)])

    def get_like_count(self):
        return self.liked_by.count()

class Like(models.Model):
    user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='liked_by'
    )

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' + self.post.title

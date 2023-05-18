from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/profile/")

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class Post(models.Model):
    post_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", null=True)
    body = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="post_dislikes", blank=True)


    def __str__(self):
        return f"{self.post_creator}: {self.body}"

    def total_likes(self):
        return self.likes.count()


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="user", blank=True)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return f"{self.user}: {self.user.id}"

class Liked(models.Model):
    user_liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_liked", null=True, blank=True)
    post_liked = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_liked", null=True, blank=True)
    is_liked = models.BooleanField(default=False)
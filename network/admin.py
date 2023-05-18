from django.contrib import admin
from .models import User, Post, UserProfile, Liked

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Liked)
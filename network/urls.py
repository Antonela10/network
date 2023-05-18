
from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profile_id>", views.user_profile, name="user_profile"),
    path("add_followers/<int:profile_id>", views.add_followers, name="add_followers"),
    path("remove_followers/<int:profile_id>", views.remove_followers, name="remove_followers"),
    path("posts_following", views.posts_following, name="posts_following"),

    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like"),
]

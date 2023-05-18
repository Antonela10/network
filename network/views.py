from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.core.serializers import serialize

from .models import User, Post, UserProfile, Liked
from .forms import PostForm


def index(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid:
            post_form = form.save(commit=False)
            post_form.post_creator = request.user
            post_form.save()
        return HttpResponseRedirect(reverse ('network:index'))
    else:
        form = PostForm()

    return render(request, "network/index.html", {
        "form": form,
        "posts": posts,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")
    

def user_profile(request, profile_id):
    profile = UserProfile.objects.get(pk=profile_id)
    profile_user = profile.user

    signed_user = UserProfile.objects.get(pk=request.user.id)
    signed_user_profile = signed_user.user
    signed_user_following = signed_user.following.all()

    posts = Post.objects.filter(post_creator = profile_user)
    posts = posts.order_by("-timestamp").all()
    followers = profile.followers.all()
    follwing = profile.following.all()
    
    user_followers_id = []
    for follower in followers:
        user_followers_id.append(follower.id)

    return render(request, "network/user_profile.html", {
        "profile": profile,
        "profile_user": profile_user,
        "posts": posts,
        "followers": followers,
        "following": follwing,
        "user_followers_id": user_followers_id,
        "signed_user_following": signed_user_following,
    })

def edit(request, post_id):
    post = Post.objects.get(pk = post_id)
    posts = list(Post.objects.all().values())
    if request.method == "GET":
        return HttpResponse(post)
    
    elif request.method == "PUT":
        POST = json.loads(request.body)
        post.body = POST['postBody']
        post.save()

        data = {
            'postBody': post.body,
        }
        return JsonResponse(data)
    
def like(request, post_id):
    user_like = request.user

    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data['id']
        post = Post.objects.get(id = post_id)
        post.save()

        if user_like not in post.likes.all():
            post.likes.add(user_like)
            post.save()
        else:
            post.likes.remove(user_like)
            post.save()

        post_likes = serialize('json', post.likes.all())

        data = {
            'post_likes': post_likes,
            'likes': post.likes.all().count(),
        }

        return JsonResponse(data)
    

# Add followers
def add_followers(request, profile_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            me = UserProfile.objects.get(pk=request.user.id)
            profile = UserProfile.objects.get(pk=profile_id)
            profile.followers.add(request.user)
            me.following.add(profile.user)
            return HttpResponseRedirect(reverse ('network:user_profile', args=(str(profile_id))))
        
# Remove followers
def remove_followers(request, profile_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            me = UserProfile.objects.get(pk=request.user.id)
            profile = UserProfile.objects.get(pk=profile_id)
            profile.followers.remove(request.user)
            me.following.remove(profile.user)
            return HttpResponseRedirect (reverse ('network:user_profile', args=(str(profile_id))))
        

def posts_following(request):
    me = UserProfile.objects.get(pk=request.user.id)
    me_following = me.following.all()
    posts = []
    followers_id = []
    for follower in me_following:
        followers_id.append(follower.id)
    all_posts = Post.objects.order_by("-timestamp").all()
    for post in all_posts:
        if post.post_creator.id in followers_id:
            posts.append(post)
    
    return render(request, "network/posts_following.html", {
        "me": me,
        "posts": posts,
    })
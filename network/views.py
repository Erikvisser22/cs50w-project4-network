import json
from operator import truediv
from queue import Empty
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.paginator import Paginator

from .models import Follower, User, Post, Like

def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by("-timestamp")
        for post in posts:
            post.likes = Like.objects.filter(post=post).count()
            if Like.objects.filter(user = request.user, post = post).count() == 0:
                post.like_from_current_user = False
            else:
                post.like_from_current_user = True

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html",{
            "all_posts" : page_obj
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def new_post(request):
    
    if request.method == "POST":
        data = json.loads(request.body)

        user = request.user
        text = data.get("text", "")

        try:
            Post.objects.create(
                user = user,
                text = text
            )
            return HttpResponseRedirect(reverse("index"), {
                "message": "Post is saved successfully."}, status=201)
        except IntegrityError:
            return JsonResponse({"error": "Not able to save post!"}, status=400)

@csrf_exempt
def profile(request, user_id):

    if request.method == "GET":
        user_profile = User.objects.get(id = user_id)
        user_posts = Post.objects.filter(user = user_profile).order_by("-timestamp")
        for post in user_posts:
            post.likes = Like.objects.filter(post=post).count()
            if Like.objects.filter(user = request.user, post = post).count() == 0:
                post.like_from_current_user = False
            else:
                post.like_from_current_user = True

        paginator = Paginator(user_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        is_following = Follower.objects.filter(user = user_profile, follower = request.user).count()
        follow_button = "Follow" if is_following == 0 else "Unfollow"
        user_likes = sum(user_posts.values_list('likes', flat=True))
        post_count = (user_posts).count()
        follower_count = Follower.objects.filter(user = user_profile).count()
        following_count = Follower.objects.filter(follower = user_profile).count()

        return render(request, "network/profile.html", {
            "user_posts" : page_obj,
            "user_profile" : user_profile,
            "follower_count" : follower_count,
            "following_count": following_count,
            "user_likes" : user_likes,
            "post_count" : post_count,
            "follow_button" : follow_button
        })

    if request.method == "PUT":
        user = request.user
        data = json.loads(request.body)
        post_owner = User.objects.get(id=data['follow_id'])

        if data['follow'] == True:
            Follower.objects.create(
                user = post_owner,
                follower = user
            )
            print("added")
        else:
            try:
                Follower.objects.filter(user=post_owner, follower=user).delete()
                print("deleted")
            except:
                print("should, but not deleted")   

        followers_count = len(Follower.objects.filter(user = post_owner))
        return JsonResponse({
            "followers_count" : followers_count
        })

def following(request, user_id): 

    if request.method == "GET":
        following = Follower.objects.filter(follower = user_id)
        followers_list =[]
        for f in following:
            followers_list.append(f.user)
        followers_posts = Post.objects.filter(user__in = followers_list).order_by("-timestamp")
        for post in followers_posts:
            post.likes = Like.objects.filter(post=post).count()
            if Like.objects.filter(user = request.user, post = post).count() == 0:
                post.like_from_current_user = False
            else:
                post.like_from_current_user = True 

        paginator = Paginator(followers_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
            
        return render(request, "network/following.html", {
            "user_posts" : page_obj,
        })

    if request.method == "PUT":
        user = request.user
        data = json.loads(request.body)
        post_owner = User.objects.get(id=data['follow_id'])

        if data['follow'] == True:
            Follower.objects.create(
                user = post_owner,
                follower = user
            )
            print("added")
        else:
            try:
                Follower.objects.filter(user=post_owner, follower=user).delete()
                print("deleted")
            except:
                print("should, but not deleted")   

        followers_count = len(Follower.objects.filter(user = post_owner))
        return JsonResponse({
            "followers_count" : followers_count
        })


@csrf_exempt
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id = post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data['like'] == True:
            Like.objects.create(
                user = user,
                post = post
            )
            print("added")
        else:
            try:
                Like.objects.filter(user=user, post=post).delete()
                print("deleted")
                
            except:
                print("should, but not deleted")
        post.like_from_current_user = data['like']
        post.likes = Like.objects.filter(post=post).count()

        return JsonResponse({
            "likes" : post.likes
        })

@csrf_exempt
def save(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id = post_id)

        data = json.loads(request.body)

        post.text = data['new_text']
        post.save()
        
        return HttpResponse(status=204)

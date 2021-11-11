from datetime import datetime
from django.utils import timezone
import django
from typing import Text
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.deletion import PROTECT
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Count, F, Q, Value
from .forms import *
from .models import *

# Create your views here.

#authentication views
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "website/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "website/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "website/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "website/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        if 'next' in request.POST:
                return redirect(request.POST['next'])
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "website/register.html")

#homepage view
def index(request):
    post1 = Post.objects.annotate(count=Count('liked')).latest('count')
    post2 = Post.objects.exclude(pk=post1.pk).annotate(count=Count('liked')).latest('count')
    excludes1 = [post1.pk, post2.pk]
    post3 = Post.objects.exclude(pk__in=excludes1).annotate(count=Count('liked')).latest('count')

    return render(request, 'website/homepage.html', {
        "post1": post1, 
        "post2": post2, 
        "post3": post3
    })
#ideas page view
def ideaboard(request):
    ideas = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(ideas, 8)
    if request.GET.get("page") != None:
        try:
            ideas = paginator.page(request.GET.get('page'))
        except:
            ideas = paginator.page(1)
    else:
        ideas = paginator.page(1)
    return render(request, 'website/ideaboard.html', {
        "ideas": ideas
    })

#post views
def post(request):
    form = AddPost()
    if request.method == 'POST':
        form = AddPost(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            saved_form = form.save()
            saved_id = saved_form.pk
            admin = User.objects.get(username='pitchyouridea')
            defcomment = Comment(user=admin, post=Post.objects.get(pk=saved_id), content='Have any queries about this idea? Leave your questions or opinions here to aid the improvement of the idea...', timestamp=datetime.now())
            defcomment.save()
            Post.objects.filter(id=saved_id).update(editedtrue='Posted')
            return redirect('/idea/{}'.format(saved_id))
    return render(request, 'website/post.html', {
        'form':form
    })

def editpost(request, post_id):
    post = Post.objects.get(id=post_id)
    form = AddPost(instance=post)
    if request.method == 'POST':
        newform = AddPost(request.POST, request.FILES, instance=post)
        if newform.is_valid():
            newform.instance.user = request.user
            saved_form = newform.save()
            saved_id = saved_form.pk
            Post.objects.filter(id=post_id).update(timestamp=datetime.now())
            Post.objects.filter(id=post_id).update(editedtrue='Edited')
            return redirect('/idea/{}'.format(saved_id))
    return render(request, 'website/post.html', {
        "form": form
    })
# subpost views
def subpost(request, post_id):
    post = Post.objects.get(id=post_id)
    subposts = Subpost.objects.filter(parentpost=post).order_by('-timestamp')
    form = AddSubPost()
    if request.method == 'POST':
        form = AddSubPost(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            new_form = form.save()
            new_form.parentpost = post
            new_form.save()
            post.updates += 1
            post.save()
            return redirect('/idea/{}'.format(post_id))
    return render(request, 'website/subpost.html', {
        "form": form, 
        "post": post, 
        "subposts": subposts
    })

def editsubpost(request, subpost_id):
    subpost = Subpost.objects.get(id=subpost_id)
    post_id = subpost.parentpost.id
    post = Post.objects.get(id=post_id)
    subposts = Subpost.objects.filter(parentpost=post).order_by('-timestamp')
    form = AddSubPost(instance=subpost)
    if request.method == "POST":
        newform = AddSubPost(request.POST, request.FILES, instance=subpost)
        if newform.is_valid():
            newform.instance.user = request.user
            saved_form = newform.save()
            Subpost.objects.filter(id=subpost_id).update(timestamp=datetime.now())
            Subpost.objects.filter(id=subpost_id).update(editedtrue='Edited')
            return redirect('/idea/{}'.format(post_id))
    return render(request, 'website/subpost.html', {
        "form": form, 
        "post": post, 
        "subposts": subposts
    })

def deletesubpost(request, subpost_id):
    subpost = Subpost.objects.filter(id=subpost_id)
    subpostinfo = Subpost.objects.get(id=subpost_id)
    post_id = subpostinfo.parentpost.id
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        subpost.delete()
        post.updates -= 1
        post.save()
        return redirect('/idea/{}'.format(post_id))
    return render(request, 'website/deletesubpost.html', {
        "subpost":subpostinfo
    })
    
#idea view
def idea(request, post_id):
    if request.method == "POST":
        postdetails = Post.objects.get(id=post_id)
        return render(request, 'website/delete.html', {
            "post": postdetails
        })
    post = Post.objects.get(id=post_id)
    subposts = Subpost.objects.filter(parentpost=post).order_by('-timestamp')
    comments = Comment.objects.filter(post=post).order_by('-timestamp')
    
    return render(request, 'website/idea.html', {
        "post": post, 
        "comments": comments, 
        "subposts": subposts, 
    })

def delete(request, post_id):
    if request.method == "POST":
        post = Post.objects.filter(id=post_id)
        post.delete()
        
        return HttpResponseRedirect(reverse('ideas'))

def like(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        likedpost = Post.objects.get(id=post_id)
        if user in likedpost.liked.all():
            likedpost.liked.remove(user)
            like = Like.objects.get(post=likedpost, user=user)
            liked = "Like"
            like.delete()
        else:
            like = Like.objects.get_or_create(post=likedpost, user=user)
            likedpost.liked.add(user)
            liked = "Liked"
            likedpost.save()
        
        data = {
            'likes': likedpost.liked.all().count(), 
            'liked': liked
        }
        return JsonResponse(data, safe=False)
    return redirect(request.META['HTTP_REFERER'])

def comment(request):
    user = request.user
    post_id = request.POST.get("post_id")
    commentedpost = Post.objects.get(id=post_id)
    if request.method == "POST":
        content = request.POST.get('comment')
        newcomment = Comment.objects.create(user=user, post=commentedpost, content=content)
        newcomment.save()
        return JsonResponse({'bool':True})
    return redirect(request.META['HTTP_REFERER'])

def delete_comment(request, comment_id):
    comment = Comment.objects.filter(id=comment_id, user=request.user)
    comment.delete()
    return redirect(request.META['HTTP_REFERER'])

def myideas(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'website/myideas.html', {
        "posts": posts
    })

#categories views
def categories(request):
    category_names = []
    for i in range(len(category_choices)):
        category_names.append(category_choices[i][0])
    category_icons = ['paint-brush', 'truck-pickup', 'swimmer', 'book', 'business-time', 'laptop-code', 'file-invoice-dollar', 'hamburger', 'dice', 'gamepad', 'heartbeat', 'skiing', 'home', 'wifi', 'user-graduate', 'gavel', 'newspaper', 'globe', 'users', 'paw', 'sign', 'asterisk', 'flask', 'shopping-cart', 'football-ball', 'plane', 'network-wired']
    return render(request, 'website/categories.html', {
        "category_names": category_names,
        "category_icons": category_icons
    })

def categoryposts(request, cats):
    category_posts = Post.objects.filter(category=cats).order_by('-timestamp')
    category_names = []
    for i in range(len(category_choices)):
        category_names.append(category_choices[i][0])
    paginator = Paginator(category_posts, 8)
    if request.GET.get("page") != None:
        try:
            category_posts = paginator.page(request.GET.get('page'))
        except:
            category_posts = paginator.page(1)
    else:
        category_posts = paginator.page(1)
    return render(request, 'website/categoryposts.html', {
        "category_posts": category_posts, 
        "cats": cats.title(),
        "category_names": category_names
    })

#leaderboard view
def leaderboard(request):
    post1 = Post.objects.annotate(count=Count('liked')).latest('count')
    post2 = Post.objects.exclude(pk=post1.pk).annotate(count=Count('liked')).latest('count')
    excludes1 = [post1.pk, post2.pk]
    post3 = Post.objects.exclude(pk__in=excludes1).annotate(count=Count('liked')).latest('count')
    excludes2 = [post1.pk, post2.pk, post3.pk]
    postsremaining = Post.objects.exclude(pk__in=excludes2).annotate(score=Count('liked')).order_by('-timestamp').order_by('-score')
    return render(request, "website/leaderboard.html", {
        "postsremaining": postsremaining, 
        "post1": post1, 
        "post2": post2, 
        "post3": post3
    })

#favourite views
def favourite(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get("post_id")
        favouritedpost = Post.objects.get(id=post_id)
        if user in favouritedpost.favourited.all():
            favouritedpost.favourited.remove(user)
            favourite = Favourite.objects.get(post=favouritedpost, user=user)
            favourited = "Track"
            favourite.delete()
        else:
            favourite = Favourite.objects.get_or_create(post=favouritedpost, user=user)
            favouritedpost.favourited.add(user)
            favourited = "Tracked"
            favouritedpost.save()
        data = {
            'favourited': favourited
        }
        return JsonResponse(data, safe=False)
    return redirect(request.META['HTTP_REFERER'])


def favouritelist(request):
    favourites = Favourite.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'website/favouritelist.html', {
        "favourites": favourites, 
    })

# private chatroom views

def allchats(request):
    chats = Chat.objects.filter(Q(owner=request.user)| Q(visitor = request.user)).order_by('-timestamp')
    return render(request, 'website/allchats.html', {
        "chats": chats
    })


def chatroom(request, post_id, owner_id, visitor_id):
    chats = Chat.objects.filter(Q(owner=request.user)| Q(visitor = request.user)).order_by('-timestamp')
    
    other_user = get_object_or_404(User, pk=owner_id)
    post = Post.objects.get(id=post_id)
    messages = Message.objects.filter(
        Q(receiver=request.user, sender=other_user, post=post)
    )
    
    messages.update(seen=True)
    messages = messages | Message.objects.filter(Q(receiver=other_user, sender=request.user, post=post))
    
    visitor = User.objects.get(id=visitor_id)
    if Chat.objects.filter(post=post, owner=visitor, visitor=other_user).exists():
        pass
    else:
        if Message.objects.filter(post=post, receiver=other_user, sender=visitor).exists():
            Chat.objects.get_or_create(post=post, owner=other_user, visitor=visitor)
    


    return render(request, "website/chatroom.html", {
        "other_user": other_user, 
        "messages": messages, 
        "post": post, 
        "visitor": visitor,
        "chats": chats, 
    })

def ajax_load_messages(request, post_id, pk):
    notif = 0
    other_user = get_object_or_404(User, pk=pk)
    post = Post.objects.get(id=post_id)
    messages = Message.objects.filter(seen=False).filter(
        Q(receiver=request.user, sender=other_user, post=post)
    )
    

    message_list = [{
        "sender": message.sender.username, 
        "message": message.message, 
        "date_created": message.date_created,
        "sent": message.sender == request.user,
    } for message in messages]
    messages.update(seen=True)
    if request.method == "POST":
        message = json.loads(request.body)    
        m = Message.objects.create(receiver=other_user, sender=request.user, message=message, post=post)
        if Message.objects.filter(receiver=other_user, sender=request.user, message=message, post=post).exists():
            if Chat.objects.filter(post=post, owner=request.user, visitor=other_user).exists():
                Chat.objects.filter(post=post, owner=request.user, visitor=other_user).update(notification='Unreplied Messages')
                Chat.objects.filter(post=post, owner=request.user, visitor=other_user).update(lastsent=request.user)
            else:
                Chat.objects.get_or_create(post=post, owner=other_user, visitor=request.user)
                Chat.objects.filter(post=post, owner=other_user, visitor=request.user).update(timestamp=datetime.now())
                Chat.objects.filter(post=post, owner=other_user, visitor=request.user).update(notification='Unreplied Messages')
                Chat.objects.filter(post=post, owner=other_user, visitor=request.user).update(lastsent=request.user)

                

        message_list.append({
            "sender": request.user.username, 
            "message": m.message, 
            "date_created": m.date_created,
            "sent": True,
        })
    return JsonResponse(message_list, safe=False)
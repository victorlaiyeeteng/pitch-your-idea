from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime, timedelta, timezone
from ckeditor.fields import RichTextField
from django.db.models.fields import BLANK_CHOICE_DASH, DateTimeField, related
from django.forms.widgets import ClearableFileInput, Widget
from django.urls import reverse
from django import forms
from django.utils.timesince import timesince

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(('email address'), unique=True)
    REQUIRED_FIELDS = ['username']






category_choices = (
    ("Arts & Entertainment", "Arts & Entertainment"),
    ("Autos & Vehicles", "Autos & Vehicles"),
    ("Beauty & Fitness", "Beauty & Fitness"),
    ("Books & Literature", "Books & Literature"),
    ("Business & Industrial", "Business & Industrial"),
    ("Computers & Electronics", "Computers & Electronics"), 
    ("Finance", "Finance"), 
    ("Food & Drink", "Food & Drink"), 
    ("Gambling & Betting", "Gambling & Betting"),
    ("Games", "Games"), 
    ("Health", "Health"), 
    ("Hobbies & Leisure", "Hobbies & Leisure"), 
    ("Home & Garden", "Home & Garden"), 
    ("Internet & Telecom", "Internet & Telecom"), 
    ("Jobs & Education", "Jobs & Education"), 
    ("Law & Government", "Law & Government"), 
    ("News", "News"), 
    ("Online Communities", "Online Communities"), 
    ("People & Society", "People & Society"), 
    ("Pets & Animals", "Pets & Animals"), 
    ("Real Estate", "Real Estate"), 
    ("Reference", "Reference"), 
    ("Science", "Science"), 
    ("Shopping", "Shopping"), 
    ("Sports", "Sports"), 
    ("Travel", "Travel"), 
    ("Others", "Others"),
)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=64, default='Untitled')
    post = RichTextField(blank=True, null=True)
    image1 = models.ImageField(blank=True, null=True, upload_to="images/")
    image2 = models.ImageField(blank=True, null=True, upload_to="images/")
    image3 = models.ImageField(blank=True, null=True, upload_to="images/")
    image4 = models.ImageField(blank=True, null=True, upload_to="images/")
    image5 = models.ImageField(blank=True, null=True, upload_to="images/")
    category = models.CharField(choices=category_choices, max_length=64, default='Others')
    timestamp = models.DateTimeField(auto_now_add=True)
    editedtrue = models.CharField(max_length=64, default='')
    updated_timestamp = models.DateTimeField(auto_now=True)
    liked = models.ManyToManyField(User, related_name="liked_user")
    favourited = models.ManyToManyField(User, related_name="favourited_user")

    def get_absolute_url(self):
        return reverse('ideas')

class Subpost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    parentpost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="parent", null=True)
    title = models.CharField(max_length=64, default='Untitled')
    post = RichTextField(blank=True, null=True)
    image1 = models.ImageField(blank=True, null=True, upload_to="images/")
    image2 = models.ImageField(blank=True, null=True, upload_to="images/")
    image3 = models.ImageField(blank=True, null=True, upload_to="images/")
    image4 = models.ImageField(blank=True, null=True, upload_to="images/")
    image5 = models.ImageField(blank=True, null=True, upload_to="images/")
    timestamp = models.DateTimeField(auto_now_add=True)
    editedtrue = models.CharField(max_length=64, default='')

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favouriteduser")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="favouritedpost", null=True)
    timestamp = models.DateTimeField(auto_now_add=True)



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likeduser")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likedpost")

class Chat(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postchat")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postowner")
    visitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postvisitor")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    notification = models.CharField(max_length=64, default='')
    lastsent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lastsentuser", null=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    seen = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postmessage", null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created", )

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifuser")
    type = models.CharField(max_length=64)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="relatedchat", null=True)


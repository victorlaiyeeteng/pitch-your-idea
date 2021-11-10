from . import views
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *
urlpatterns = [
    path("", views.index, name="index"), 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path('post/', views.post, name='post'),
    path('editpost/<int:post_id>', views.editpost, name="editpost"),
    path('update/<int:post_id>', views.subpost, name='subpost'),
    path('editupdate/<int:subpost_id>', views.editsubpost, name='editsubpost'),
    path('deleteupdate/<int:subpost_id>', views.deletesubpost, name='deletesubpost'),
    path("ideas/", views.ideaboard, name='ideas'), 
    path("idea/<int:post_id>", views.idea, name='idea'), 
    path("myideas/", views.myideas, name='myideas'), 
    path("delete/<int:post_id>", views.delete, name='delete'), 
    path("like", views.like, name="like"), 
    path("comment", views.comment, name="comment"), 
    path("delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"), 
    path('favourite', views.favourite, name='favourite'),
    path('favouritelist', views.favouritelist, name='favouritelist'),
    path("categories/<str:cats>/", views.categoryposts, name='category'),
    path("categories", views.categories, name='categories'), 
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("allchats", views.allchats, name="allchats"),
    path("<int:post_id>/<int:owner_id>/<int:visitor_id>", views.chatroom, name="chatroom"),
    path("ajax/<int:post_id>/<int:pk>/", views.ajax_load_messages, name="chatroom-ajax"), 
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), #home page
    path("login", views.login_view, name="login"), #login page 
    path("logout", views.logout_view, name="logout"), #logout page
    path("register", views.register, name="register"), #register page
    path("uploadimage/<int:profile_id>", views.upload_image, name="upload_image"), #change profile picture and bio
    path("profile/<int:profile_id>", views.profile_view, name="profile" ), #view an account
    path("create", views.create_view, name = "create"), #function to process new posts
    path("follow/<int:profile_id>", views.follow, name = "follow"), #path for following accounts
    path("following", views.following, name="following"), #view following page
    path("editpost/<int:post_id>", views.editpost, name="edit"), #path for editing posts 
    path("following_profile/<int:profile_id>", views.following_profile, name="following_profile"), #path to view followings
    path("follower_profile/<int:profile_id>", views.follower_profile, name = "follower_profile"), #path to view followers
]

#define a URL pattern in Django, takes 3 arguments, URL pattern, view function to be called, name for the pattern
#name="following_profile": This is an optional argument that gives a name to the URL pattern. Naming URL patterns is useful when generating URLs in templates or redirecting within your Django application.
#<int:post_id> is a path converter. It specifies that the part of the URL after "following_profile/" should be an integer, 
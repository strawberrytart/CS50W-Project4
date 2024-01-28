from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_image = models.ImageField(upload_to = 'network/profile_images/', blank = True, null=True, default="network/profile_images/icon.jpg")
    banner = models.ImageField(upload_to= 'network/banner/', blank=True, null=True)
    following = models.ManyToManyField('self', blank = True, null = True, symmetrical = False, related_name = "follower")
    bio = models.TextField(blank = True, null = True, max_length = 160)

    # we need to set symmetrical to False, because the default value is True and when its true, if A follows B, automatically the database 
    # will register B follows A, which is not the correct paradigm. If Alice follows Bob, it does not mean Bob follows Alice.
    # so its not symmetrical.

    def __str__(self):
        return self.username
    
    def count_following(self):
        return self.following.count()
    
    def count_follower(self):
        return self.follower.count()
    
    def serialize(self):
        return{
            "id": self.id,
            "following": self.count_following(),
            "followers": self.count_follower(),
        }
    
class Post(models.Model): #Create a model called Post,inheriting from Django's models.Model
    body = models.TextField(max_length = 280)
    timestamp = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')
    #Establishing a M:1 relationship between Post and User, when user is deleted, delete all related post, and find all post related to user
    likes = models.ManyToManyField(User, blank= True, null = True, related_name = 'likes')

    def __str__(self):#provides instructions for how to turn a Post object into a string
        return self.body
    
    def count_likes(self):
        return self.likes.count()

class Comments(models.Model):
    body = models.TextField(max_length = 280)
    timestamp = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.body


#blank = True means the form fields can be blank, form validation allows an empty value
    
#null = True sets NULL to the columns of your DB
    
#CharFields and TextFields, which in Django are never saved as NULL. Blank values are stored in the DB as an empty string (''). 
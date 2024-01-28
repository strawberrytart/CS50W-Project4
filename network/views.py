import json 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import EditProfileForm, PostForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post


def index(request): #home page
    #Get all the posts and order them by date, recent posts come first
    posts = Post.objects.all().order_by('-timestamp')
    # Show only 10 posts per page
    paginator = Paginator(posts, 10)
    #Get the current page number
    page_number = request.GET.get('page')
    #Show the posts on that current page number
    page_obj = paginator.get_page(page_number) 
    # create an instance of class named PostForm()
    post_form = PostForm()

    return render(request, "network/index.html",{
        "page_obj": page_obj,
        "post_form": post_form,
        "paginator":paginator,
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


@login_required(login_url='login')
def upload_image(request, profile_id):
    # if request is POST, save the user uploaded image
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data["profile_image"]
            bio = form.cleaned_data["bio"]
            user = User.objects.get(id=request.user.id)

            #Get the default image path specified in ImageField
            default_profile_image_path = User._meta.get_field('profile_image').get_default()
            # If the uploaded image is not the same as the default image path, set the user's profile image to the uploaded image
            if image != default_profile_image_path:
                user.profile_image = image
            #Update the user's bio
            user.bio = bio
            #Save changes.
            user.save()
            #Redirect active user to the profile page
            return HttpResponseRedirect(reverse("profile", args=(profile_id,)))
        else:
            return render(request, "network/profile.html", {
                "form":form,
            })
    #If page accessed via GET request, just show the profile page of interest
    return HttpResponseRedirect(reverse("profile", args=(profile_id,)))


def profile_view(request, profile_id):
    #Get the profile currently in view
    try:
        profile = User.objects.get(id = profile_id)
    except User.DoesNotExist:
        profile = None
        message = "Account does not exist."
        return render(request, "network/error.html",{
            "message": message,
        })
    
    else:#when there is no error
        posts = profile.posts.all().order_by('-timestamp')

    #Get the user that is logged in 
    try: 
        user = User.objects.get(id = request.user.id)
    except User.DoesNotExist:
        user = None
    
    #Initialize following as False, 
    following = False
    #We want to show the follow and unfollow button only if there is an active user
    #Following is a flag that allows us to check if the profile of interest is currently followed by the active user or not
    if request.user.is_authenticated:
        if profile in user.following.all():
            following = True
        else:
            following = False
    
    #Instantiate the EditProfileForm with prepopulated bio information
    editProfileForm = EditProfileForm(initial = {"bio" : profile.bio})
    #Create an instance of the PostForm()
    post_form = PostForm()
    return render(request, "network/profile.html",{
        "profile": profile,
        "posts": posts,
        "following": following,
        "editProfileForm": editProfileForm,
        "post_form": post_form,
    })

@login_required(login_url='login')
def create_view(request):
    #When the post form is submitted
    if request.method == "POST":
        #Take in the data the user submitted and save it as form 
        form = PostForm(request.POST)
        #Check if form data is valid (server side)
        if form.is_valid():
            #Save the form data without committing it to a database, allowing for further modifications
            post = form.save(commit = False)
            #Set the poster field of the post to the active user 
            post.poster = request.user 
            #save and hit the database
            post.save()
            #Redirect to the index page
            return HttpResponseRedirect(reverse('index'))
        
    #If page is accessed via GET request, redirect user to the index page
    return HttpResponseRedirect(reverse('index'))

@csrf_exempt
def follow(request,profile_id):
    # If PUT request
    if request.method == "PUT":
        #Get the logged in user
        user = User.objects.get(id= request.user.id)
        #Deserialize JSON data from the request body
        data = json.loads(request.body)
        #Get the profile of interest
        profile = User.objects.get(id=profile_id)

        if data.get("action") == "follow":
            #Check if account is already being followed
            if profile in user.following.all():
                print("Account already being followed")
                return JsonResponse({"error": "Account already being followed"}, status = 400)

            else:
                #If not followed, add profile to the user's following field
                user.following.add(profile)
                print(f"Successfully followed {profile.username}")
                return JsonResponse(profile.serialize())

        elif data.get("action") == "unfollow":
            # If profile is not being followed, return error
            if profile not in user.following.all():
                print("You weren't even following this account in the first place.")
                return JsonResponse({"error":"Cannot unfollow account that isn't followed"}, status = 400)
                
            else:
                #If being followed, remove profile from user's following field
                user.following.remove(profile)
                print(f"Successfully unfollowed {profile.username}")
                return JsonResponse(profile.serialize())
    else:
        return JsonResponse({"error": "PUT request required."}, status = 400)



@login_required(login_url ='/login')
def following(request):
    #Get the user object of the logged in user 
    user = User.objects.get(id = request.user.id)
    #Get the accountst the user is currently following
    following = user.following.all()
    #Get the posts made by the users that the logged in user is following
    #Django ORM, the double underscore '__' is used as a lookup type to perform complex queries 
    #Check if the owner of the post is in the 'following' queryset
    posts = Post.objects.filter(poster__in = following).order_by('-timestamp')

    #Create a Paginator object that allows 10 posts per page
    paginator = Paginator(posts, 10)
    #Get the current page number
    page_number = request.GET.get('page')
    #Get a specific page and show the posts on that page
    page_obj = paginator.get_page(page_number) 

    post_form = PostForm()
    return render(request, "network/following.html",{
        "post_form": post_form,
        "page_obj": page_obj,
        "paginator": paginator,
    })

    #renders a HTML template, takes in HTTP request, template name and dictionary context as data 


@csrf_exempt
def editpost(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status = 400)
    
    try:
        #Get the post that is being edited
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=400)
    
    #Deserialize JSON data from the request body
    data = json.loads(request.body)
    
    #Retrieve the value associated with the key "content" from the parsed JSON data
    if data.get("content"):
        #If the active user is not the owner of the post
        if post.poster != request.user:
            return JsonResponse({"error": "Unauthorized edit."}, status = 401)
        
        #If the content length is more than 280 characters 
        elif len(data["content"]) > 280:
            return JsonResponse({"error": "Invalid post length."}, status = 400)
        #Update the post body and save it
        else:
            post.body = data["content"]
            post.save()
            return JsonResponse({"message": "Email sent successfully."}, status = 201)
    
    #Retrive value associated with "action" from the parsed JSON data
    if data.get("action"):
        #Get the post being liked or unlike
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error":"Post not found."}, status = 400)
        #Get the logged in user
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return JsonResponse({"error":"User does not exists."}, status = 400)
        
        #If the action is like, checking if post is currently liked or not
        if data.get("action") == "like":
            if user in post.likes.all():
                print(f"{user.username} already like this post")
                return JsonResponse({"error":"Cannot like a post twice"}, status = 400)
            #Add user to the post's like 
            else:
                post.likes.add(user)
                print(post.likes.all())
                return JsonResponse({"like_count": post.likes.count()}, status = 201)

        #If the action is to unlike, checking if post is currently like or not
        elif data.get("action") == "unlike":
            if user in post.likes.all():
                post.likes.remove(user)
                return JsonResponse({"like_count": post.likes.count()}, status = 201)
            else:
                print(f"Cannot unlike post. Like didn't exist!")
                return JsonResponse({"error":"Cannot unlike a post not liked."}, status = 400)
    return JsonResponse({"error": "Method doesn't match"}, status = 400)

#Show the profile's following 
def following_profile(request,profile_id):
    try:
        profile = User.objects.get(id= profile_id)
    except User.DoesNotExist:
        profile = None
        message = "Account does not exist."
        return render(request, "network/error.html",{
            "message" : message,
        })
    
    following = profile.following.all()

    return render(request, "network/following_profile.html",{
        "following": following,
        "profile": profile,
    })

#Show the profile's followers
def follower_profile(request, profile_id):
    try:
        profile = User.objects.get(id = profile_id)
    except User.DoesNotExist:
        profile = None
        message = "Account does not exist."
        return render(request, "network/error.html",{
            "message" : message,
        })
    
    followers = profile.follower.all()

    return render(request, "network/follower_profile.html",{
        "followers": followers,
        "profile": profile,
    })


        
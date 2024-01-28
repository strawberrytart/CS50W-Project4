from django.forms import ModelForm
from .models import User, Post
from django import forms

class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["profile_image", "bio"]

        widgets ={
            'bio' : forms.Textarea(attrs={"class":"form-control", "id":"edit_bio"}),
        }

       
        labels ={
            "profile_image": "Photo",
            "bio": "Bio"
        }

class PostForm(ModelForm):
    class Meta:
        model = Post    
        fields = ["body"]

        widgets = {
            'body': forms.Textarea(attrs={"class":"form-control"}),
        }
        labels = {
            'body':"",
        }

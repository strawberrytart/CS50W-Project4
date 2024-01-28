from django.contrib import admin

# Register your models here.

from .models import User, Post, Comments

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("following",)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ["body", "commenter", "post"]


class PostAdmin(admin.ModelAdmin):
    list_display = ["body", "timestamp", "poster"]
    filter_horizontal = ("likes",)

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)
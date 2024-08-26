from django.contrib import admin
from .models import Profile_User, Post, LikePost, FollowersCount, Comments

# Register your models here.

admin.site.register(Profile_User)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Comments)
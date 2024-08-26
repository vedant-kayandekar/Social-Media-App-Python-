from django.db import models
from django.contrib.auth import get_user_model  
import uuid
from datetime import datetime
 # ye jo get_user_model hai voh inbiuld def function hai jo ham use karenge user se input linekeleye


User = get_user_model()
# ab iss function ko variable me dala so ham isee import karkeke views mai use kar sakte haii


# Create your models here.

class Profile_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture-973460_1280.png')  #YE Defautly profile banate samay sab kon ek default img chipkadekaga  Issse ka main kamm - ye media folder mai ek profile-images karke folder create karega jab koi profile photo ko update karne jayega eg.sample.png, aur uska address kesa hoga -(profile_images/sample.png)
    location = models.CharField(max_length=100, blank=True)

   
    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posr_images')
    caption = models.TextField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user
    
class FollowersCount2(models.Model):
    follower2 = models.CharField(max_length=100)
    user2 = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user2
    
class Comments(models.Model):
    product = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    commenter_name = models.ForeignKey(Profile_User, related_name="profile", on_delete=models.CASCADE)
    comment_body = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' %(self.product.id, self.commenter_name)
    


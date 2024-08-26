from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
# from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Profile_User
from .models import Post, LikePost, FollowersCount, Comments
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from itertools import chain
from .forms import CommentForm
import random
import datetime








# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile_User.objects.get(user=user_object)
  
    user_following_list =[]
    feed =[]
   
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_lists = list(chain(*feed)) 

    # #user seggestion starts
    # all_users = User.objects.all()
    # user_following_all = []

    # for user in user_following:
    #     user_list = User.objects.get(username=user.user)
    #     user_following_all.append(user_list)

    # new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]   
    # current_user = User.objects.filter(username=request.user.username)
    # final_suggestion_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))] 
    # random.shuffle(final_suggestion_list) 

    # username_profile = [] 
    # username_profile_list = [] 

    # for users in final_suggestion_list:
    #     username_profile.append(users.id)

    # for ids in username_profile:
    #     profile_lists = Profile_User.objects.filter(id_user=ids)

    # suggestions_username_profile_list = list(chain(*username_profile_list))       

    # posts = Post.objects.all()
    # return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_lists, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]} )

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile_User.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    # if request.method == "POST":
    #     add_comment_form = CommentForm(request.Post)
    #     if add_comment_form.is_valid():
    #         add_comment_form.save()
    #     else:
    #         add_comment_form = CommentForm()

    # context = {
    #     "add_comment_form":add_comment_form,
    # }        
    
    

    
    
    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_lists, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')    
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile_User.objects.get(user=user_object)
    
    if request.method =='POST':
       username = request.POST['username'] 
       username_object = User.objects.filter(username__icontains=username)

       username_profile = []
       username_profile_list = []

       for users in username_object:
           username_profile.append(users.id)

       for ids in username_profile:
           profile_lists = Profile_User.objects.filter(id_user=ids)  
           username_profile_list.append(profile_lists)  
 
       username_profile_list = list(chain(*username_profile_list))   
    return render(request, 'search.html',{'user_profile': user_profile, 'username_profile_list': username_profile_list })    

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile_User.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_grid_mai_all_post_ayenge = Post.objects.all()
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text ='Unfollow'
    else:
        button_text ='Follow'   
    
    # follower and following
    user_follower = len(FollowersCount.objects.filter(user=pk))    
    user_following = len(FollowersCount.objects.filter(follower=pk))    

    context = {
        'user_profile' : user_profile,
        'user_object' : user_object,
        'user_posts' : user_posts,
        'user_posts_grid_mai_all_post_ayenge' : user_posts_grid_mai_all_post_ayenge,
        'user_post_length' :user_post_length,
        # 'user_profile': user_profile
        'button_text': button_text,
        'user_follower' : user_follower,
        'user_following' : user_following,

    }

    # user_profile2 = Profile_User.objects.get(user=request.user)

    # if request.method == 'POST':
     
    #   if request.Files.get('image') == None:
    #       image = user_profile2.profileimg

    #       user_profile2.profileimg = image
    #       user_profile2.save()
      
    #   if request.FILES.get('image') != None:
    #       image = request.FILES.get('image')

    #       user_profile2.profileimg = image
    #       user_profile2.save()

    #   return redirect('/')
             
    return render(request, 'profile.html', context )

@login_required(login_url='signin')
def profile2(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile_User.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_grid_mai_all_post_ayenge = Post.objects.all()
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text ='Unfollow'
    else:
        button_text ='Follow'   
    
    # follower and following
    user_follower = len(FollowersCount.objects.filter(user=pk))    
    user_following = len(FollowersCount.objects.filter(follower=pk))    

    context = {
        'user_profile' : user_profile,
        'user_object' : user_object,
        'user_posts' : user_posts,
        'user_posts_grid_mai_all_post_ayenge' : user_posts_grid_mai_all_post_ayenge,
        'user_post_length' :user_post_length,
        # 'user_profile': user_profile
        'button_text': button_text,
        'user_follower' : user_follower,
        'user_following' : user_following,

    }

    # user_profile2 = Profile_User.objects.get(user=request.user)

    # if request.method == 'POST':
     
    #   if request.Files.get('image') == None:
    #       image = user_profile2.profileimg

    #       user_profile2.profileimg = image
    #       user_profile2.save()
      
    #   if request.FILES.get('image') != None:
    #       image = request.FILES.get('image')

    #       user_profile2.profileimg = image
    #       user_profile2.save()

    #   return redirect('/')
             
    return render(request, 'profile2.html', context )



def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')    
        
def follow2(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile2/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile2/'+user)
    else:
        return redirect('/')        

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile_User.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings') 
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                print(user_model)
                print(username)
                new_profile = Profile_User.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    print(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        # messages.info(request, 'Crccccccccccccccc')
        return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')



# def homee(request):
#     stories = []

#     for user in Profile_User.objects.all():
#         items = []
#         for status in user.status.all():
#             items.append({
#                 "id":"",
#                 "type":"",
#                 "length":"3",
#                 "src":"/media/{status.file}",
#             })
#         stories.append({
#             "id": user.id,
#             "photo": f'/media/{user.photo}',
#             "name": user.name,
#         })
    
#     return render(request,'home.html',context = {'stories':json.dumps(stories)})

        

def add_comment(request,pk):
    eachPost = Post.objects.get(id=pk)

    form = CommentForm(instance=eachPost)
    if request.method == "POST":
        form = CommentForm(request.POST,instance=eachPost)
        name = request.user.username
        body = form.cleaned_data['comment_body']

        c = Comments(product=eachPost, commenter_name=name, comment_body=body, date_commented=datetime.now())
        c.save()

        return redirect('index')
    else:
        form = CommentForm()

    context = {
        "form":form,
    }

    return render(request, 'add_comment.html',context)      
    




from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from .models import Profile, Post, Like, FollowerCount
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.urls import reverse
from django.contrib.messages import get_messages
import json

# @login_required(login_url='signin')
def index(request):
    try:
        if 'login_status' not in request.COOKIES:
            return redirect('signin')
        username = request.COOKIES['username']
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)

        user_following_list = []
        feed = []

        user_following = FollowerCount.objects.filter(follower=username)
        for user in user_following:
            user_following_list.append(user.user)

        for usernames in user_following_list:
            feed_list = Post.objects.filter(user=usernames)
            feed.append(feed_list)

        feed_list = list(chain(*feed))

        post = Post.objects.all()
        return render(request, "base.html", {'user_profile': profile, 'posts': feed_list, 'username': username})
    except Exception as e:
        messages.error(request, 'An error occurred while performing the main page. Error: {e}')
        return redirect('/')

# @login_required(login_url='signin')
def post(request,id_post):
    if 'login_status' not in request.COOKIES:
        return redirect('signin')
    try:
        username = request.COOKIES['username']
        post = Post.objects.get(id_post=id_post, user=username)
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)

        context = {
            'post': post,
            'user_profile': profile
        }

        return render(request, 'post.html', context)
    except Exception as e:
        messages.error(request, 'An error occurred while performing the post page. Error: {e}')
        return redirect('/')

# @login_required(login_url='signin')
def likes(request):
    if 'login_status' not in request.COOKIES:
        return redirect('signin')
    try:
        user = request.COOKIES['username']
        id_post = request.GET.get('post_id')

        post = Post.objects.get(id_post=id_post)

        first_like = Like.objects.filter(id_post=id_post, user=user).first()

        if first_like is None:
            new_like = Like.objects.create(id_post=id_post, user=user)
            new_like.save()
            post.likes += 1
            post.save()
            return redirect('/')
        else:
            first_like.delete()
            post.likes -= 1
            post.save()
            return redirect('/')    
    except Exception as e:
        messages.error(request, f'An error occurred while performing the like operation. Error: {e}')
        return redirect('/')    

# @login_required(login_url='signin')
def logout(request):
    if 'login_status' not in request.COOKIES:
        return redirect('signin')
    response = redirect('signin')
    response.delete_cookie('username')
    response.delete_cookie('login_status')
    auth.logout(request)
    return response

# @login_required(login_url='signin')
def follow(request):
    if 'login_status' not in request.COOKIES:
        return redirect('signin')
    try:
        if request.method == 'POST':
            follower = request.POST['follower']
            user = request.POST['user']
            # print('follower: '+follower+' user: '+user)
            user_follow = FollowerCount.objects.filter(user=user, follower=follower).first()

            if user_follow is None:
                new_follow = FollowerCount.objects.create(user=user, follower=follower)
                new_follow.save()
                messages.success(request, 'Followed')
                return redirect('/profile/'+user)
            else:
                user_follow.delete()
                messages.success(request, 'Unfollowed')
                return redirect('/profile/'+user)
        else:
            return redirect('/')
    except Exception as e:
        messages.error(request, f'An error occurred while performing the follow operation. Error: {e}')
        return redirect('/')

# @login_required(login_url='signin')
def search(request):
    if 'login_status' not in request.COOKIES:
        return redirect('signin')
    try:
        user_object = User.objects.get(username=request.COOKIES['username'])
        user_profile = Profile.objects.get(user=user_object)

        if request.method == 'POST':
            username = request.POST['search']
            username_object = User.objects.filter(username__icontains=username)

            username_profile = []
            username_profile_list = []

            for users in username_object:
                if users != user_object:
                    username_profile.append(users.id)

            for ids in username_profile:
                profile_lists = Profile.objects.filter(id_user=ids)
                username_profile_list.append(profile_lists)
            
            username_profile_list = list(chain(*username_profile_list))
        return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
    except Exception as e:
        messages.error(request, f'An error occurred while performing the search operation. Error: {e}')
        return redirect('/')

# @login_required(login_url='signin')
def profile(request, username):
    if 'login_status' not in request.COOKIES:
        return redirect('signin')
    try:
        if username is None:
            username = request.user.username
        login_user = User.objects.get(username=request.COOKIES['username'])
        user_obj = User.objects.get(username=username)
        profile = Profile.objects.get(user=user_obj)
        post = Post.objects.filter(user=username)
        len_post = len(post)

        follower = request.user.username
        user = username

        if FollowerCount.objects.filter(user=user, follower=follower).first():
            button_text = 'Unfollow'
        else:
            button_text = 'Follow'

        user_followers = len(FollowerCount.objects.filter(user=user))
        user_following = len(FollowerCount.objects.filter(follower=user))
        
        context = {
            'user_profile': profile,
            'login_user': login_user,
            'user_object': user_obj,
            'user_posts': post,
            'user_len_post': len_post,
            'button_text': button_text,
            'user_followers': user_followers,
            'user_following': user_following
        }
        return render(request, 'profile.html', context)
    except Exception as e:
        messages.error(request, f'An error occurred while performing the profile page. Error: {e}')
        return redirect('/')

# @login_required(login_url='signin')
def upload(request):
    if 'login_status' not in request.COOKIES:
        return redirect('signin')
    if request.method == 'POST':
        try:
            image = request.FILES.get('image_upload')
            caption = request.POST['caption']
            user = request.COOKIES['username']
            user_img = Profile.objects.get(user=User.objects.get(username=user)).profileimg

            new_post = Post.objects.create(user=user, image=image, caption=caption, user_img=user_img)
            new_post.save()
            messages.success(request, 'Post uploaded successfully')
            return redirect('/')
        except Exception as e:
            messages.error(request, f'An error occurred while performing the upload operation. Error: {e}')
            return redirect('/')
    else:
        return render('/')

# @login_required(login_url='signin')
def settings(request):
    if 'login_status' not in request.COOKIES:
        return redirect('signin')
    try:
        user_object = User.objects.get(username=request.COOKIES['username'])
        user_profile = Profile.objects.get(user=user_object)
        user_posts = Post.objects.filter(user=request.COOKIES['username'])

        if request.method == 'POST':
            
            if request.FILES.get('image') == None:
                image = user_profile.profileimg
            
            elif request.FILES.get('image') != None:
                image = request.FILES.get('image')
            print(image)
            bio = request.POST['bio']
            birthday = request.POST['birthday']
            for post in user_posts:
                post.user_img = image
                post.save()
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.birthday = birthday
            user_profile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile/'+request.COOKIES['username'])
        return render(request, 'settings.html', {'user_profile': user_profile})
    except Exception as e:
        messages.error(request, f'An error occurred while performing the settings page. Error: {e}')
        return redirect('/')

def signin(request):
    if 'login_status' in request.COOKIES:
        return redirect('/')
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']

            # lodin
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)

                response = redirect('/')

                response.set_cookie('username', username, secure=True)
                response.set_cookie('login_status', True, max_age=60*60*24*30)
                messages.success(request, 'Login successfully')
                return response
            else:
                messages.info(request, 'Invalid credentials')
                return redirect('signin')
        except Exception as e:
            messages.error(request, f'An error occurred while performing the signin operation. Error: {e}')
            return redirect('signin')
    else:
        return render(request, "signin.html")

def signup(request):
    if 'login_status' in request.COOKIES:
        return redirect('/')
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('signup')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Account created successfully')
                    # lodin after signup
                    user = auth.authenticate(username=username, password=password)
                    auth.login(request, user)
                    response = redirect('/') 

                    # create profile
                    user_loged = User.objects.get(username=username)
                    users_profile = Profile.objects.create(user=user_loged, id_user=user_loged.id)
                    users_profile.save()
                    response.set_cookie('username', username)
                    response.set_cookie('login_status', True, max_age=60*60*24*30)
                    return response
                    # return redirect('/')
            else:
                messages.error(request, 'Password not matching')
                return redirect('signup')
        except Exception as e:
            messages.error(request, f'An error occurred while performing the signup operation. Error: {e}')
            return redirect('signup')
    else:
        return render(request, "signup.html")

# @login_required(login_url='signin')
def delete_profile(request):
    if 'login_status' not in request.COOKIES:
        return redirect('signin')
    if request.method == 'POST':
        try:
            username = request.COOKIES['username']
            user_object = User.objects.get(username=username)
            user_profile = Profile.objects.get(user=user_object)
            user_posts = Post.objects.filter(user=username)
            users_likes = Like.objects.filter(user=user_object)
            users_followers = FollowerCount.objects.filter(user=username)
            users_following = FollowerCount.objects.filter(follower=username)
            for post in user_posts:
                post.delete()
            for like in users_likes:
                like.delete()
            for follower in users_followers:
                follower.delete()
            for following in users_following:
                following.delete()
            user_profile.delete()
            user_object.delete()
            response = redirect('signin')
            response.delete_cookie('username')
            response.delete_cookie('login_status')
            messages.success(request, 'Delete profile successfully')
            return response
        except Exception as e:
            messages.error(request, f'An error occurred while performing the delete account operation. Error: {e}')
            return redirect('/')
    storage = get_messages(request)
    messages_list = [{'level': message.tags, 'text': message.message} for message in storage]
    messages_json = json.dumps(messages_list)

    # return render(request, 'delete_account.html', {'messages_json': messages_json})
    return render(request, 'confirm_delete.html', {
        'object_type': 'profile',
        'cancel_url': reverse('settings'), 
        'messages_json': messages_json 
    })

# @login_required(login_url='signin')
def delete_post(request, id_post):
    if 'login_status' not in request.COOKIES:
        return redirect('signin')
    if request.method == 'POST':
        try:
            username = request.COOKIES['username']
            post = Post.objects.get(id_post=id_post, user=username)
            post.delete()
            messages.success(request, 'Delete post successfully')
            return redirect('/')
        except Exception as e:
            messages.error(request, f'An error occurred while performing the delete post operation. Error: {e}')
            return redirect('/')
    return render(request, 'confirm_delete.html', {
        'object_type': 'post',
        'cancel_url': '../', 
    })

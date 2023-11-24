from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from .models import Profile, Post, Like
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def index(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)

    post = Post.objects.all()
    return render(request, "index.html", {'user_profile': profile, 'posts': post})

@login_required(login_url='signin')
def likes(request):
    user = request.user.username
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

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='signin')
def profile(request):
    return render(request, 'profile.html')
@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        user = request.user.username

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return render('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
        
        elif request.FILES.get('image') != None:
            image = request.FILES.get('image')
        
        bio = request.POST['bio']
        birthday = request.POST['birthday']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.birthday = birthday
        user_profile.save()
        
        return redirect('settings')
    return render(request, 'settings.html', {'user_profile': user_profile})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # lodin
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')
    else:
        return render(request, "signin.html")

def signup(request):
    if request.method == 'POST':
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

                # lodin after signup
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)

                # create profile
                user_loged = User.objects.get(username=username)
                users_profile = Profile.objects.create(user=user_loged, id_user=user_loged.id)
                users_profile.save()
                return redirect('/')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
    else:
        return render(request, "signup.html")
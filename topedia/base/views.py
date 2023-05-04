# 2101940 Kyle Keene-Welch
# views.py
# Creates various function based views to render templates and perform back-end processing.

from django.shortcuts import render, redirect
from django.db.models import Q
from . models import Room, Topic, Message, User, UserFollowing, UserFavourites, LearningMaterial
from . forms import RoomForm, RegisterForm, LoginForm, MaterialForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

# Authenticates user
def loginPage(request):
    page = 'login'
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid:
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                user = User.objects.get(email=email)       
            except:
                messages.error(request, 'User does not exist')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('home')
            else:
                messages.error(request, 'Username or password does not exist')
        else:
            messages.error(request, 'An error occured during Login')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

# Logs out user
def logoutUser(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('home')

# Registers user
def registerPage(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password_Confirmation']:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.set_password(user.password)
                user.save()
                login(request, user)

                newFollowing = UserFollowing()
                newFollowing.user = user
                newFollowing.save()

                newFavourites = UserFavourites()
                newFavourites.user = user
                newFavourites.save()

                messages.success(request, 'Registration Successful')
                return redirect('home')
            else:
                messages.error(request, 'Passwords do not match')
        else:
            messages.error(request, 'Form input not valid.')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)

# Renders home page with associated content
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    favourites = None
    if request.user.is_authenticated:
        if UserFavourites.objects.get(user=request.user.id):
            object = UserFavourites.objects.get(user=request.user.id)
            favourites = object.rooms.all()
        else:
            messages.error(request, 'No Favourites')

    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages': room_messages, 'favourites': favourites}
    return render(request, 'base/home.html', context)

# Renders a selected room with associated content
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        messages.success(request, 'Message Added')
        return redirect('room', pk=room.id)

    favourites = None
    if request.user.is_authenticated:
        if UserFavourites.objects.get(user=request.user.id):
            object = UserFavourites.objects.get(user=request.user.id)
            favourites = object.rooms.all()
        else:
            messages.error(request, 'No Favourites')
    
    learningMaterial = room.learningMaterial.all()

    context = {'room': room, 'room_messages': room_messages, 'participants': participants, 'favourites': favourites, 'learningMaterial': learningMaterial}
    return render(request, 'base/room.html', context)

# Shows list of user topic room favourites
@login_required(login_url='login')
def showFavourites(request, pk):
    _user = User.objects.get(id=pk)
    if UserFavourites.objects.get(user=pk):
        object = UserFavourites.objects.get(user=pk)
        rooms = object.rooms.all()
    else:
        messages.error(request, 'No Favourites')

    favourites = rooms
    context = {'user': _user, 'rooms': rooms, 'favourites': favourites}
    return render(request, 'base/favourites.html', context)

# Shows list of users the user follows
@login_required(login_url='login')
def showFollowers(request):
    if UserFollowing.objects.get(user=request.user.id):
        object = UserFollowing.objects.get(user=request.user.id)
        following = object.following.all()
    else:
        messages.error(request, 'No User Following')

    context = {'user': request.user, 'following': following}
    return render(request, 'base/following.html', context)

# Displays the users profile and associated content
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    if UserFollowing.objects.get(user=request.user.id):
        object = UserFollowing.objects.get(user=request.user.id)
        if object.following.contains(user):
            following = True
        else:
            following = False

        if request.method == 'POST':
            if request.POST.get('status') == "setFollow":
                object.following.add(user)
                messages.success(request, 'User Followed')
                return redirect('user-profile', pk=user.id)
            else:
                object.following.remove(user)
                messages.success(request, 'User Unfollowed')
                return redirect('user-profile', pk=user.id)
    else:
        messages.error(request, 'No User Following')

    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    favourites = None
    if request.user.is_authenticated:
        if UserFavourites.objects.get(user=request.user.id):
            object = UserFavourites.objects.get(user=request.user.id)
            favourites = object.rooms.all()
        else:
            messages.error(request, 'No Favourites')

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics, 'following': following, 'favourites': favourites}
    return render(request, 'base/profile.html', context)

# Sets a topic room as a favourite
@login_required(login_url='login')
def setFavourite(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        if UserFavourites.objects.get(user=request.user.id):
            object = UserFavourites.objects.get(user=request.user.id)
            object.rooms.add(room)
        else:
            messages.error(request, 'No Favourites')
    else:
        messages.error(request, 'Invalid Action')
    messages.success(request, 'Topic Room is now a favourite')

    if request.META.get('HTTP_REFERER') != None: 
            return redirect(request.META.get('HTTP_REFERER'))  
    else:
            return redirect('home')

# Creates a new topic room
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    formName = "createRoom"
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic = Topic.objects.get_or_create(name=topic_name)

        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.topic = topic[0]
            room.save()
            messages.success(request, 'Topic Room Created')
            return redirect('home')
    context = {'form': form, 'formName': formName, 'topics': topics}
    return render(request, 'base/display_form.html', context)

# Creates some new learning material
@login_required(login_url='login')
def createMaterial(request, pk):
    form = MaterialForm()
    formName = "createMaterial"
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user
            material.save()
            room.learningMaterial.add(material)
            messages.success(request, 'Learning Material Created')
            return redirect('home')
    context = {'form': form, 'formName': formName}
    return render(request, 'base/display_form.html', context)

# Updates a user account
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    formName = "updateUser"

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password_Confirmation']:
                updatedUser = form.save(commit=False)
                updatedUser.set_password(updatedUser.password)
                updatedUser.save()
                login(request, updatedUser)
                messages.success(request, 'Account Updated')
                return redirect('user-profile', pk=user.id)
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Form input not valid.')
    context = {'form':form, 'formName': formName}
    return render(request, 'base/display_form.html', context)

# Updates some learning material
@login_required(login_url='login')
def updateMaterial(request, pk):
    material = LearningMaterial.objects.get(id=pk)
    form = MaterialForm(instance=material)
    formName = "updateMaterial"
    if request.user != material.user:
        return HttpResponse('You are not the owner of this learning material')

    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid:
            form.save()
            messages.success(request, 'Changes were successful')
            return redirect('home')
    context = {'form':form, 'formName': formName}
    return render(request, 'base/display_form.html', context)

# Updates a topic room
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    topic = room.topic
    form = RoomForm(instance=room)
    formName = "updateRoom"
    if request.user != room.host:
        return HttpResponse('You are not the owner of this topic room')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic = Topic.objects.get_or_create(name=topic_name)

        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            room = form.save(commit=False)
            room.topic = topic[0]
            room.save()
            messages.success(request, 'Changes were successful')
            return redirect('home')
    context = {'form':form, 'formName': formName, 'topics': topics, 'topic': topic}
    return render(request, 'base/display_form.html', context)

# Deletes a topic room
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not the owner of this topic room')

    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Topic room deleted successfully')
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

# Deletes a message
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not the owner of this message')
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully')
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

# Removes a topic room as a favourite
@login_required(login_url='login')
def removeFavourite(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        if UserFavourites.objects.get(user=request.user.id):
            object = UserFavourites.objects.get(user=request.user.id)
            object.rooms.remove(room)
            messages.success(request, 'Topic room is no longer a favourite')
        else:
            messages.error(request, 'No Favourites')
    else:
        messages.error(request, 'Invalid Action')
    if request.META.get('HTTP_REFERER') != None: 
            return redirect(request.META.get('HTTP_REFERER'))  
    else:
            return redirect('home')

# Unfollows a user
@login_required(login_url='login')
def unfollow(request, pk):
    user = User.objects.get(id=pk)
    follower = UserFollowing.objects.get(user=request.user.id)
    if request.method == 'POST':
        follower.following.remove(user)
        messages.success(request, 'User has been unfollowed')
        return redirect('show-following')

# Deletes some learning material
@login_required(login_url='login')
def deleteMaterial(request, pk):
    material = LearningMaterial.objects.get(id=pk)
    if request.user != material.user:
        return HttpResponse('You are not the owner of this learning material')
    if request.method == 'POST':
        if material.image:
            material.image.delete()
        material.delete()
        messages.success(request, 'Learning Material deleted successfully')
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':material.heading})

# Shows the topics page with list of topics
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

# Shows the activity page with list of recent activity
def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
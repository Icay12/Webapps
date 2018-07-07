# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.db import transaction
from socialnetwork.forms import RegistrationForm, CreatePost, GlobalPostForm, ProfileForm, CreateProfileForm
from socialnetwork.models import *
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

# def home_page(request):
#     context = {'display': 0, 'newValue': 0, 'preValue': 0, 'preOperation': '+', 'preButton': 1, 'errors': []}
#     return render(request, 'socialnetwork/homepage.html', context)


@login_required
def global_stream(request):
    entries = list(Post.objects.all().order_by('-creation_time'))
    return render(request, 'socialnetwork/globalstream.html', {'entries': entries})


@login_required
def follower_stream(request, username):
    print username
    thisuser = User.objects.get(username=username)
    follow = Follow.objects.filter(ouser=username)
    follower = []
    newentries = []

    for f in follow:
        follower.append(f.iuser)
    entries = list(Post.objects.order_by('-creation_time'))

    for e in entries:
        if e.user.username in follower:
            newentries.append(e)
    return render(request, 'socialnetwork/followerstream.html', {'entries': newentries})


@login_required
def profile(request, username):

    try:
        thisuser = User.objects.get(username=username)
        profile = Profile.objects.get(user=thisuser)

        profileform = ProfileForm(instance=profile)
        followlist = list(Follow.objects.filter(ouser=thisuser.username))

        if request.user.is_authenticated() and thisuser.id == request.user.id:
            userself = True

            if request.method == 'GET':
                context = {'profile': profile, 'form': profileform, 'userself': userself,'followlist': followlist}
                return render(request, 'socialnetwork/profile.html', context)

            entry = Profile.objects.select_for_update().get(username=username)
            form = ProfileForm(request.POST, request.FILES, instance=entry)
            if not form.is_valid():
                context = {'profile': entry, 'form': form, 'userself': userself, 'followlist': followlist}
                return render(request, 'socialnetwork/profile.html', context)

            entry.content_type = form.cleaned_data['img']
            form.save()


            context = {
                'message': 'Profile updated.',
                'profile': entry,
                'form': form,
                'userself': userself,
                'followlist': followlist,
            }
            return render(request, 'socialnetwork/profile.html', context)


    except Profile.DoesNotExist:
        context = {'message': 'Record with id={0} does not exist'.format(id)}
        return render(request, 'socialnetwork/profile.html', context)


@login_required
def otherprofile(request, username):

    try:

        if request.user.is_authenticated():
            thisuser = User.objects.get(username=username)
            profile = Profile.objects.get(user=thisuser)

            cnt = Follow.objects.filter(iuser=thisuser.username, ouser=request.user.username).count()
            if cnt == 0:
                isfollow = False
            else:
                isfollow = True

            followlist = list(Follow.objects.filter(ouser=thisuser.username))

            if thisuser == request.user:
                profileform = ProfileForm(instance=profile)
                context = {'profile': profile , 'form': profileform, 'userself': True, 'followlist': followlist}
                return render(request, 'socialnetwork/profile.html', context)


            if request.method == 'GET':
                context = {'profile': profile, 'thisuser': thisuser, 'followlist': followlist, 'isfollow': isfollow}
                return render(request, 'socialnetwork/otherprofile.html', context)

            if request.method == 'POST':
                if isfollow:
                    Follow.objects.filter(iuser=thisuser.username, ouser=request.user.username).delete()
                else:

                    newfollow = Follow(iuser=thisuser.username, ouser=request.user.username)
                    newfollow.save()

                isfollow = not isfollow
                followlist = Follow.objects.filter(ouser=thisuser.username).all()
                context = {'profile': profile, 'thisuser': thisuser, 'followlist': followlist,
                            'isfollow': isfollow}

                return render(request, 'socialnetwork/otherprofile.html', context)



    except Profile.DoesNotExist:
        context = {'message': 'Record with id={0} does not exist'.format(id)}
        return render(request, 'socialnetwork/otherprofile.html', context)



@login_required
def create(request):

    # Adds the new item to the database if the request parameter is present
    if 'newPost' not in request.POST or not request.POST['newPost']:
        message ='You must enter something to post.'
    else:
        new_entry = Post(post=request.POST['newPost'],
                        creation_time=timezone.now())
        new_entry.user = request.user
        new_entry.save()
        message = 'Post created'

    # Sets up data needed to generate the view, and generates the view

    entries = list(Post.objects.all().order_by('-creation_time'))

    # new_post = CreatePost(dummy_entry)
    # context = { 'message': message, 'entry': dummy_entry, 'form': new_post }
    context = {'message': message, 'entries': entries}

    return render(request, 'socialnetwork/globalstream.html', context)





def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    profile = Profile(last_name=new_user.last_name, first_name=new_user.first_name, username=new_user.username,bio="", img=None)
    profile.user = new_user
    profile.save()
    # print profile.username
    return redirect(reverse('home'))


def get_photo(request, id):
    item = get_object_or_404(Profile, user_id=id)
    # print "get item"
    # Probably don't need this check as form validation requires a picture be uploaded.
    if not item.img:
        # print "404"
        raise Http404
    # print "before return"
    return HttpResponse(item.img)



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
from django.core import serializers
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail


# def home_page(request):
#     context = {'display': 0, 'newValue': 0, 'preValue': 0, 'preOperation': '+', 'preButton': 1, 'errors': []}
#     return render(request, 'socialnetwork/homepage.html', context)


@login_required
def global_stream(request):
    # entries = list(Post.objects.all().order_by('-creation_time'))
    # return render(request, 'socialnetwork/globalstream.html', {'entries': entries})
    return render(request, 'socialnetwork/globalstream.html', {})
    # response_text = serializers.serialize('json', Post.objects.all().order_by('-creation_time'))
    # return HttpResponse(response_text, content_type='application/json')


@login_required
def follower_stream(request, username):
    # thisuser = User.objects.get(username=username)
    # follow = Follow.objects.filter(ouser=username)
    # follower = []
    # newentries = []
    #
    # for f in follow:
    #     follower.append(f.iuser)
    # entries = list(Post.objects.order_by('-creation_time'))
    #
    # for e in entries:
    #     if e.user.username in follower:
    #         newentries.append(e)
    # return render(request, 'socialnetwork/followerstream.html', {'entries': newentries})
    return render(request, 'socialnetwork/followerstream.html', {})


@transaction.atomic
@login_required
def profile(request, username):
    try:
        with transaction.atomic():
            thisuser = User.objects.get(username=username)
            profile = Profile.objects.get(user=thisuser)

            profileform = ProfileForm(instance=profile)
            followlist = list(Follow.objects.filter(ouser=thisuser.username))

            if request.user.is_authenticated() and thisuser.id == request.user.id:
                userself = True

                if request.method == 'GET':
                    context = {'profile': profile, 'form': profileform, 'userself': userself, 'followlist': followlist}
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


@transaction.atomic
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
                context = {'profile': profile, 'form': profileform, 'userself': True, 'followlist': followlist}
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


# @login_required
# def create(request):
#
#     # Adds the new item to the database if the request parameter is present
#     if 'newPost' not in request.POST or not request.POST['newPost']:
#         message ='You must enter something to post.'
#     else:
#         new_entry = Post(post=request.POST['newPost'],
#                         creation_time=timezone.now())
#         new_entry.user = request.user
#         new_entry.save()
#         message = 'Post created'
#
#     # Sets up data needed to generate the view, and generates the view
#
#     entries = list(Post.objects.all().order_by('-creation_time'))
#
#     # new_post = CreatePost(dummy_entry)
#     # context = { 'message': message, 'entry': dummy_entry, 'form': new_post }
#     context = {'message': message, 'entries': entries}
#
#     return render(request, 'socialnetwork/globalstream.html', context)

@login_required
def create(request):
    if request.method != 'POST':
        raise Http404

    if not 'newPost' in request.POST or not request.POST['newPost']:
        message = 'You must enter something to post.'
        json_error = '{ "error": "' + message + '" }'
        return HttpResponse(json_error, content_type='application/json')

    new_entry = Post(post=request.POST['newPost'], creation_time=timezone.now())
    new_entry.user = request.user
    new_entry.name = request.user.username
    new_entry.save()
    message = 'Post created'

    response_text = serializers.serialize('json', Post.objects.all().order_by('-creation_time'))
    # response_text = serializers.serialize('json', new_entry)
    return HttpResponse(response_text, content_type='application/json')


@login_required
def addcomment(request):
    # print "here"
    if request.method != 'POST':
        raise Http404
    if not 'newComment' in request.POST or not request.POST['newComment']:
        message = 'You must enter something to comment.'
        json_error = '{ "error": "' + message + '" }'
        # print "notnew"
        return HttpResponse(json_error, content_type='application/json')
    post_id = request.POST.get('post_id')

    newComment = request.POST.get('newComment')

    post = Post.objects.get(id=post_id)

    new_comment = Comment(text=newComment, date=timezone.now())
    new_comment.user = request.user
    new_comment.username = request.user.username
    new_comment.owner = post
    new_comment.ownerid = post_id
    new_comment.save()
    # print "save"
    comment = Comment.objects.all().filter(owner=post)
    response = serializers.serialize('json', list(comment), fields=('comment-list'))

    return HttpResponse(response, content_type='application/json')


def get_changes(request, time="1970-01-01T00:00:00.000Z"):
    max_time = Post.get_max_time()
    posts = Post.get_changes(time)
    comments = []
    for each in posts:
        comment = Comment.objects.filter(owner=each.id)
        comments.append(comment)
        context = {"max_time": max_time, "posts": posts, "comments": comments}
    return render(request, 'posts.json', context, content_type='application/json')


@transaction.atomic
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
    new_user.is_active = False
    new_user.save()

    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
    Please click the link below to verify your email address and
    complete the registration of your account:

      http://{host}{path}
    """.format(host=request.get_host(),
               path=reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="kxie1@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    profile = Profile(last_name=new_user.last_name, first_name=new_user.first_name, username=new_user.username, bio="",
                      img=None)
    profile.user = new_user
    profile.save()
    return render(request, 'socialnetwork/needs-confirmation.html', context)


    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'])

    # login(request, new_user)
    # profile = Profile(last_name=new_user.last_name, first_name=new_user.first_name, username=new_user.username,bio="", img=None)
    # profile.user = new_user
    # profile.save()
    # # print profile.username
    # return redirect(reverse('home'))


@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()

    return render(request, 'socialnetwork/confirmed.html', {})


def get_photo(request, id):
    item = get_object_or_404(Profile, user_id=id)
    # print "get item"
    # Probably don't need this check as form validation requires a picture be uploaded.
    if not item.img:
        # print "404"
        raise Http404
    # print "before return"
    return HttpResponse(item.img)


def get_list_json(request):
    # print "post"
    response_text = serializers.serialize('json', Post.objects.all().order_by('-creation_time'))
    return HttpResponse(response_text, content_type='application/json')


def get_comment_list_json(request):
    post_id = request.GET['post_id']
    # print "here"
    # print post_id
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.filter(owner=post)
    response_text = serializers.serialize('json', comment)
    return HttpResponse(response_text, content_type='application/json')


def get_list_xml(request):
    response_text = serializers.serialize('xml', Post.objects.all())
    return HttpResponse(response_text, content_type='application/xml')


def get_list_xml_template(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'socialnetwork/posts.xml', context, content_type='application/xml')


def get_follow_list_json(request):
    # print "post"
    thisuser = request.user
    follow = Follow.objects.filter(ouser=thisuser.username)
    follower = []
    newentries = []

    for f in follow:
        follower.append(f.iuser)
    entries = list(Post.objects.order_by('-creation_time'))

    for e in entries:
        if e.user.username in follower:
            newentries.append(e)
    response_text = serializers.serialize('json', newentries)
    return HttpResponse(response_text, content_type='application/json')

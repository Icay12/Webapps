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

from socialnetwork.forms import RegistrationForm, CreatePost, GlobalPostForm


# def home_page(request):
#     context = {'display': 0, 'newValue': 0, 'preValue': 0, 'preOperation': '+', 'preButton': 1, 'errors': []}
#     return render(request, 'socialnetwork/homepage.html', context)


@login_required
def global_stream(request):
    gentries = []
    gentry1 = TRUMP_ENTRY
    gentry2 = JANE_ENTRY
    # if entry == None:
    #     context = { 'message': 'Record with id={0} does not exist'.format(id) }
    #     return render(request, 'socialnetwork/globalstream.html', context)

    # Fill in dummy time and user data
    # gentry['creation_time'] = "February 12, 2018 - 04:56:26"
    # print gentry['created_by']

    # gform = GlobalPostForm(gentry)
    gentry1['comments'] = []
    gentry1['comments'].append(OBAMA_COMMENT)
    gentries.append(gentry1)
    gentries.append(gentry2)
    context = {'gentries': gentries}
    return render(request, 'socialnetwork/globalstream.html', context)


@login_required
def follower_stream(request):
    gentries = []
    gentry1 = USER1_ENTRY
    gentry2 = JANE_ENTRY
    # if entry == None:
    #     context = { 'message': 'Record with id={0} does not exist'.format(id) }
    #     return render(request, 'socialnetwork/globalstream.html', context)

    # Fill in dummy time and user data
    # gentry['creation_time'] = "February 12, 2018 - 04:56:26"
    # print gentry['created_by']

    # gform = GlobalPostForm(gentry)
    gentry1['comments'] = []
    gentry1['comments'].append(USER2_COMMENT)
    gentries.append(gentry1)
    gentries.append(gentry2)
    context = {'gentries': gentries}
    return render(request, 'socialnetwork/followerstream.html', context)


@login_required
def profile(request):
    thisuser = USER1
    # if entry == None:
    #     context = { 'message': 'Record with id={0} does not exist'.format(id) }
    #     return render(request, 'socialnetwork/globalstream.html', context)

    # Fill in dummy time and user data
    # gentry['creation_time'] = "February 12, 2018 - 04:56:26"
    # print gentry['created_by']

    # gform = GlobalPostForm(gentry)

    context = {'thisuser': thisuser}
    return render(request, 'socialnetwork/profile.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        context = { 'form': CreatePost() }
        return render(request, 'socialnetwork/globalstream.html', context)

    create_post = CreatePost(request.POST)
    if not create_post.is_valid():
        context = { 'form': create_post }
        return render(request, 'socialnetwork/globalstream.html', context)

    dummy_entry = {}
    for field in [ 'post' ]:
        dummy_entry[field] = create_post.cleaned_data[field]

    dummy_entry['created_by']    = request.user
    dummy_entry['creation_time'] = timezone.now()

    message = 'Post created'
    new_post = CreatePost(dummy_entry)
    context = { 'message': message, 'entry': dummy_entry, 'form': new_post }
    return render(request, 'socialnetwork/globalstream.html', context)





def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
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

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))



TRUMP_ENTRY = {
    'id': 45,
    'last_name':    'Trump',
    'first_name':   'Donald',
    'creation_time': 'February 12, 2018 - 04:56:26',
    'post':      'Hello everyone, this is my first post on Blog Master, follow me please.'
}


JANE_ENTRY = {
    'id': 5,
    'last_name':    'Doe',
    'first_name':   'Jane',
    'creation_time': 'February 02, 2018 - 18:32:10',
    'post':      'Guess what my name is. hhhhhhh'
}


USER1_ENTRY = {
    'id': 5,
    'last_name':    'Xie',
    'first_name':   'Ke',
    'creation_time': 'February 05, 2018 - 13:08:55',
    'post':      'I am so Saaaaaaaaaaaaad'
}

OBAMA_COMMENT = {
    'last_name': 'Barack',
    'first_name': 'Obama',
    'creation_time': 'February 12, 2018 - 05:57:30',
    'comm': "No, I won't"
}

USER2_COMMENT = {
    'last_name': 'Xia',
    'first_name': 'Shelly',
    'creation_time': 'February 06, 2018 - 00:12:46',
    'comm': "Everything's gonna be fine."
}


USER2 = {
    'last_name': 'Xia',
    'first_name': 'Shelly',
    'bios': "Anything is possible",
    'followers': []
}

USER3 = {
    'last_name': 'Trump',
    'first_name': 'Donald',
    'bios': "I am No.1",
    'followers': []
}

USER1 = {
    'last_name': 'Xie',
    'first_name': 'Ke',
    'image': "sample/Sample.png",
    'bio': 'Nothing is impossible',
    'followers': [USER2 , USER3]
}


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, Http404
from django.core import serializers
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

import random, string
from datetime import datetime, timedelta
from django.utils import timezone
import pytz

from uiop.forms import RegistrationForm
from uiop.models import Channel, File





# Create your views here.
# def home(request):
#     return render(request, 'uiop/home.html', {})
#
#
#

@csrf_exempt
def create_channel(request):
    req = json.loads(request.body.decode("utf-8").replace('\0', ''))

    code = str(generate_channel_code())
    password = req['password']

    create_time = timezone.now()
    display_create_time = timezone.make_naive(create_time).strftime("%Y-%m-%d %H:%M:%S")
    expire_time = (create_time + timezone.timedelta(minutes=30))
    display_expire_time = timezone.make_naive(expire_time).strftime("%Y-%m-%d %H:%M:%S")

    if req['mode'] is False:
        mode = False
    else:
        mode = True


    username = req['owner']


    channel = Channel(channel_code=code, password= password, create_time=create_time, expire_time=expire_time, mode= mode, owner_id=username, active = True, online_number= 0)

    channel.save()

    # result = {}
    # result['channel_code'] = code
    # result['expirationTime'] = expire_time
    # result['creationTime'] = create_time
    # result['owner'] = username
    # result['lecturerMode'] = mode

    response_text = '{"channel_code": "' + code + '", "channel_online_number":"' + "0" + '", "expirationTime":"' + str(display_expire_time) + '","creationTime":"'+str(display_create_time)+'",'+ '"owner":"' +username +'", "lecturerMode":"' +str(mode) + ' "}'

    # print response_text
    return HttpResponse(response_text, content_type='application/json')





def generate_channel_code():

    code = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(4))

    while Channel.objects.filter(channel_code=code).exists():
        code = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(4))
    return code


@csrf_exempt
def enter_channel(request, code):
    if request.method == 'GET':
        username = request.GET['username']
        channel = Channel.objects.filter(channel_code = code)
        if len(channel) == 0 or channel[0].active is False:
            result = '{"success" : "false", "message" : "Channel not Exists!"}'
            return HttpResponse(result, content_type='application/json')

        else:
            channel = channel[0]

        if username != channel.owner_id and len(channel.password)>0:# TODO this need to test
            result = '{"success" : "false", "needPassword" : "true"}'
            return HttpResponse(result, content_type='application/json')

        else:
            newfiles = list(File.objects.filter(channel_code=code).order_by('-upload_time'))

            newfile_list = "["

            index = 0
            while index < len(newfiles):
                if index != 0:
                    newfile_list += ","
                file = newfiles[index]
                myfile = '{"fileName": "' + file.file_name + '", "fileID" : "' + str(file.id) + '", "fileAddress":"' + str(file.file_address) + '", "fileType":"' + file.file_type + '", "downloadTimes":"' + str(file.download_times)  + '", "fileSize":"' + file.file_size + '", "uploadTime":"' + str(file.upload_time) + ' "}'
                index = index + 1
                newfile_list += myfile
            newfile_list += "]"

            create_time = channel.create_time
            display_create_time = timezone.make_naive(create_time).strftime("%Y-%m-%d %H:%M:%S")
            expire_time = channel.expire_time
            display_expire_time = timezone.make_naive(expire_time).strftime("%Y-%m-%d %H:%M:%S")

            response_text = '{"lecturerMode": "' + str(channel.mode) + '", "channel_online_number":"' + str(channel.online_number) + '", "expirationTime":"' + str(display_expire_time) + '","creationTime":"' + str(display_create_time) + '",' + '"owner":"' + channel.owner_id + '","newfileList":' + newfile_list + ', "password" : "'+ channel.password +'"}'


            # result = '{"lecturerMode" : true, "expirationTime" : "15", "creationTime" : "15"}'
            return HttpResponse(response_text, content_type='application/json')

    #input password
    else:
        req = json.loads(request.body.decode("utf-8").replace('\0', ''))
        password = req['password']
        channel = Channel.objects.filter(channel_code = code)[0]
        if channel.password == password:
            newfiles = list(File.objects.filter(channel_code=code).order_by('-upload_time'))

            newfile_list = "["

            index = 0
            while index < len(newfiles):
                if index != 0:
                    newfile_list += ","
                file = newfiles[index]
                myfile = '{"fileName": "' + file.file_name + '", "fileID" : "' + str(file.id) + '", "fileAddress":"' + str(file.file_address) + '", "fileType":"' + file.file_type + '", "downloadTimes":"' + str(file.download_times)  + '", "fileSize":"' + file.file_size + '", "uploadTime":"' + str(file.upload_time) + ' "}'
                index = index + 1
                newfile_list += myfile
            newfile_list += "]"

            create_time = channel.create_time
            display_create_time = timezone.make_naive(create_time).strftime("%Y-%m-%d %H:%M:%S")
            expire_time = channel.expire_time
            display_expire_time = timezone.make_naive(expire_time).strftime("%Y-%m-%d %H:%M:%S")

            response_text = '{"lecturerMode": "' + str(channel.mode) + '", "channel_online_number":"' + str(channel.online_number) + '", "expirationTime":"' + str(display_expire_time) + '","creationTime":"' + str(display_create_time) + '",' + '"owner":"' + channel.owner_id + '","newfileList":' + newfile_list + '}'

            return HttpResponse(response_text, content_type='application/json')
        else:
            response_text = '{"errorMessage": "' + "Wrong Password!" + ' "}'
            return HttpResponse(response_text, content_type='application/json')


@csrf_exempt
def pull_new_file(request, code):

    # code = req['channel_code']
    # timestamp = datetime.utcfromtimestamp(req['timestamp']/1000).replace(tzinfo=pytz.utc)

    # now = timezone.now()

    # newfiles = list(File.objects.filter(channel_code=code).filter(upload_time__range=(timestamp, now)).order_by('-upload_time'))

    newfiles = list(File.objects.filter(channel_code=code).order_by('-upload_time'))
    newfile_list = "["

    index = 0
    while index < len(newfiles):
        if index != 0:
            newfile_list += ","
        file = newfiles[index]
        myfile = '{"fileName": "' + file.file_name + '", "fileID" : "' + str(file.id) + '", "fileAddress":"' + str(file.file_address) + '", "fileType":"' + file.file_type + '", "downloadTimes":"' + str(file.download_times) + '", "fileSize":"' + file.file_size + '", "uploadTime":"' + str(file.upload_time.strftime("%Y-%m-%d %H:%M:%S")) + ' "}'
        index = index + 1
        newfile_list += myfile
    newfile_list += "]"

    response_text = '{"newfileList": ' + newfile_list + ' }'
    return HttpResponse(response_text, content_type='application/json')


def update_channel_info(request, code):
    channel = Channel.objects.filter(channel_code=code)[0]

    expire_time = channel.expire_time
    display_expire_time = timezone.make_naive(expire_time).strftime("%Y-%m-%d %H:%M:%S")

    response_text = '{"lecturerMode": "' + str(channel.mode) + '", "expirationTime":"' + str(display_expire_time) +  '","active":"' + str(channel.active) + '","channel_online_number":"' + str(channel.online_number) + ' "}'
    return HttpResponse(response_text, content_type='application/json')


def expire():
    now = timezone.now()

    channels = Channel.objects.filter(active=True).filter(expire_time__lte = now)
    for channel in channels:
        channel.active = False
        channel.save()

    return ""

@csrf_exempt
def add_person(request, code):

    channels = Channel.objects.filter(channel_code=code)
    if len(channels) == 0 or channels[0].active is False:
        result = '{"success" : "false", "message" : "Channel not Exists!"}'
        return HttpResponse(result, content_type='application/json')
    channel = channels[0]
    person = channel.online_number
    channel.online_number = person + 1
    channel.save()

    response_text = '{"channel_online_number": "' + str(channel.online_number) + '"}'
    return HttpResponse(response_text, content_type='application/json')

@csrf_exempt
def minus_person(request, code):
    channels = Channel.objects.filter(channel_code=code)

    if len(channels) == 0 or channels[0].active is False:
        result = '{"success" : "false", "message" : "Channel not Exists!"}'
        return HttpResponse(result, content_type='application/json')
    channel = channels[0]

    person = channel.online_number
    channel.online_number = person - 1
    channel.save()

    response_text = '{"channel_online_number": "' + str(channel.online_number) + '"}'
    return HttpResponse(response_text, content_type='application/json')

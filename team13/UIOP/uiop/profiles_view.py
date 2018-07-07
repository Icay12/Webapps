from __future__ import unicode_literals

import json
from uiop.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from uiop.models import Channel

@csrf_exempt
def modify_password(request):
    req = json.loads(request.body.decode("utf-8").replace('\0',''))
    username = req['username']
    old = req['old']
    new = req['new']
    if old == new:
        result = '{"success" : "false", "message" : "Old password is the same as new password"}'
        return HttpResponse(result,  content_type='application/json')
    user = User.objects.filter(username=username)
    if len(user) == 0:
        result = '{"success" : "false", "message" : "User not found"}'
        return HttpResponse(result,  content_type='application/json')
    if user[0].password != old:
        result = '{"success" : "false", "message" : "Old password is wrong."}'
        return HttpResponse(result,  content_type='application/json')
    user[0].password = new
    user[0].save()
    result = '{"success" : "true", "message" : "Password modified successfully"}'
    return HttpResponse(result,  content_type='application/json')

@csrf_exempt
def show_channel_list(request):
    req = json.loads(request.body.decode("utf-8").replace('\0',''))
    username = req['username']
    channel_list = Channel.objects.filter(owner_id = username).filter(active=True)
    result = '{'
    if len(channel_list) == 0:
        result += '"success" : "true" , "message" : "empty list"}'
        return HttpResponse(result,  content_type='application/json')
    index = 0
    ch_list = "["
    while index < len(channel_list):
        if index != 0:
            ch_list += ","
        ch = channel_list[index]
        iter = '{"channelCode" : "' + ch.channel_code + '", "expireTime" : "' + str(ch.expire_time) + '"}'
        ch_list += iter
        index += 1
    ch_list += "]"
    result += '"channelList" : '+ ch_list
    result += '}'
    return HttpResponse(result, "application/json")

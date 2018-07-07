from __future__ import unicode_literals

import json
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse, Http404
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.utils import timezone

from uiop.models import Channel, File

@csrf_exempt
def modify_channel(request,code):
    req = json.loads(request.body.decode("utf-8").replace('\0', ''))
    channel = Channel.objects.filter(channel_code=code)[0]
    username = req['username']

    if username != channel.owner_id:  # TODO this need to test
        result = '{"success" : "false", "message" : "Not Channel Owner!"}'
        return HttpResponse(result, content_type='application/json')


    password = req['password']
    if password != "":
        Channel.objects.filter(channel_code=code).update(password = password)

    if req['mode'] == "false":
        mode = False
    else:
        mode = True
    Channel.objects.filter(channel_code=code).update(mode=mode)


    if req['expire_time'] != "":
        extend = int(req['expire_time'])
        expire_time = (timezone.now()+timedelta(minutes=extend))
        Channel.objects.filter(channel_code=code).update(expire_time=expire_time)

    channel = Channel.objects.filter(channel_code=code)[0]
    display_expire_time = timezone.make_naive(channel.expire_time).strftime("%Y-%m-%d %H:%M:%S")
    response_text = '{"mode": "' + str(channel.mode)+ '", "password":"' + channel.password + '", "expire_time":"' + str(display_expire_time) + '","active":"' + str(channel.active) + ' "}'

    return HttpResponse(response_text, content_type='application/json')


@csrf_exempt
def expire_now(request, code):
    channel = Channel.objects.filter(channel_code=code)
    if len(channel) == 0 or channel[0].active is False:
        response_text = '{"success": "' + "false" + '", "message":"' + "No Such Channel" + ' "}'
    else:
        Channel.objects.filter(channel_code=code).update(active = False)
        response_text = '{"success": "' + "true" + '", "message":"' + "Expire Successfully" + ' "}'

    return HttpResponse(response_text, content_type='application/json')
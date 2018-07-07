# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import login, authenticate
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse, Http404, QueryDict
from django.core import serializers
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt
from uiop.models import User
import hashlib
import datetime

@csrf_exempt
def register(request):
    result = {}

    #TODO needs validation
    req = json.loads(request.body.decode("utf-8").replace('\0',''))
    username = req['username']
    password = req['password']

    u = User.objects.filter(username=username)
    if len(u) != 0:
        result = '{"success" : false, "message" : "the username is already used"}'
        return HttpResponse(result,  content_type='application/json')

    token = username+str(datetime.datetime.now())
    new_user = User(username=username, password=password, token=token)

    new_user.save()

    result = '{"success" : true, "token" : "'+token+'"}'
    return HttpResponse(result, content_type='application/json')

@csrf_exempt
def login(request):
    req = json.loads(request.body.decode("utf-8").replace('\0',''))
    username = req['username']
    password = req['password']
    u = User.objects.filter(username = username)
    if len(u) == 0 :
        result = '{"success" : false, "message" : "username not exists"}'
        return HttpResponse(result, content_type='application/json')
    if u[0].password != password:
        result = '{"success" : false, "message" : "password is wrong"}'
        return HttpResponse(result, content_type='application/json')
    token = username+str(datetime.datetime.now())
    u[0].token = token
    u[0].save()
    result = '{"success" : true, "token" : "'+ token+'"}'
    return HttpResponse(result, content_type='application/json')

def checkLogin(username, token):
    result = {}
    u = User.objects.filter(username = username)
    if len(u) == 0 :
        result["success"] = False
        result["message"] = "user not exist"
        return result
    tk = u[0].token
    if tk == token:
        result["success"] = True
        return result


from __future__ import unicode_literals

import datetime
import json
import os

import sys
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse, Http404
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime
from django.utils import timezone

from uiop.models import File, Channel

@csrf_exempt
def upload(request, code):
    f = request.FILES.get("file", "")
    if f:
        fc = ContentFile(f.read())
    else:
        result = '{"success" : "false", "message" : "File is empty"}'
        return HttpResponse(result,  content_type='application/json')
    size = ""
    acsize = fc.size
    if fc.size < 1000000:
        size = str(fc.size/1000)+"KB"
    else:
        size = str(fc.size/1000)+"MB"
    name = str(f)
    tp = name.split('.')
    tp = tp[len(tp) - 1]
    if tp == "docx" or tp == "doc":
        tp = "word"
    elif tp == "jpg" or tp == "png":
        tp = "image"
    elif tp == "ppt" or tp == "pptx":
        tp = "powerpoint"
    elif tp == "xls" or tp == "xlsx":
        tp = "excel"
    elif tp == "zip" or tp == "rar":
        tp = "archive"
    elif tp == "txt":
        tp = "alt"

    time = timezone.now()
    file = File(file_address = f, file_name = name, file_size = size, channel_code = code, upload_time = time, file_type=tp, actual_size=acsize)
    file.save()
    add = str(file.file_address)
    result = '{"success" : "true", "message" : "upload successfully", "fileName" : "' + name + '", "fileID" : "' + str(file.id) + '", "fileSize" : "' + size + '", "fileType" : "' + tp + '", "fileAddress" : "' + add + '"}'
    return HttpResponse(result,  content_type='application/json')

@csrf_exempt
def download(request, id):
    fileid = id  # file is actually its id
    fo = File.objects.filter(id=fileid)
    if len(fo) == 0:
        result = '{"success" : "false", "message" : "File not Exists!"}'
        return HttpResponse(result, content_type='application/json')

    code = fo[0].channel_code
    channels = Channel.objects.filter(channel_code=code)

    if len(channels) == 0 or channels[0].active is False:
        result = '{"success" : "false", "message" : "Channel not Exists!"}'
        return HttpResponse(result, content_type='application/json')


    def readFile(fn, buf_size = 262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()


    fileadd = str(fo[0].file_address)
    size = fo[0].actual_size
    name = fo[0].file_name
    fobj = fo[0]
    fobj.download_times = fobj.download_times + 1
    fobj.save()
    # f = File.objects.filter(file_address=fileadd, channel_code=code)
    # if not f[0].file_address:
    #     return Http404git
    response = HttpResponse(readFile(fileadd), content_type='application/octet-stream')
    response['Content-disposition'] = 'attachment; filename=' + name
    response['Content-Length'] = size
    return response

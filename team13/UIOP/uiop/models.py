# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# from django.contrib.auth.models import User

#User (defined by django)


class Channel(models.Model):
    channel_code = models.CharField(max_length=4, primary_key=True)
    password = models.CharField(max_length=20, blank=True)
    create_time = models.DateTimeField()
    expire_time = models.DateTimeField()
    mode = models.BooleanField()
    owner_id = models.CharField(max_length=20, default="")
    active = models.BooleanField()
    online_number = models.IntegerField(default=0)


class File(models.Model):
    file_address = models.FileField(upload_to="file", blank=True)
    file_name = models.CharField(max_length=20, default="")
    file_size = models.CharField(max_length=20, default="")
    file_type = models.CharField(max_length=20, default="")
    channel_code = models.CharField(max_length=4, default="")
    upload_time = models.DateTimeField()
    actual_size = models.IntegerField(default=0)
    download_times = models.IntegerField(default=0)


class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
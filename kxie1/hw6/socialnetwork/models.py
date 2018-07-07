# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max



class Post(models.Model):
    post = models.CharField(max_length=4200)
    user = models.ForeignKey(User, default=None)
    name = models.CharField(max_length=4200, default="username")
    creation_time = models.DateTimeField()

    @staticmethod
    def get_max_time():
        return Post.objects.all().aggregate(Max('date'))['date__max'] or "1970-01-01T00:00:00.000Z"

    @staticmethod
    def get_changes(time="1970-01-01T00:00:00.000Z"):
        return Post.objects.filter(date__gt=time).distinct()


class Profile(models.Model):
    last_name = models.CharField(max_length=20, default="lastname")
    first_name = models.CharField(max_length=20, default="firstname")
    username = models.CharField(max_length=20, default="username")
    user = models.OneToOneField(User, unique=True, related_name='social_network_profiles')
    bio = models.CharField(max_length=200, blank=True, default=None)
    img = models.FileField(upload_to="images", blank=True, default=None)


class Follow(models.Model):
    # iuser : users be followed
    # ouser : users following
    iuser = models.CharField(max_length=20)
    ouser = models.CharField(max_length=20)


class Comment(models.Model):
    owner = models.ForeignKey(Post, default="")
    user = models.ForeignKey(User, default="")
    text = models.CharField(max_length=420)
    date = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=420, default="username")
    ownerid = models.CharField(max_length=20,default="1")







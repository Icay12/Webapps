# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Data model for a todo-list item
class Post(models.Model):
    post = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None)
    # post = models.CharField(blank=True, max_length=200)
    # created_by = models.ForeignKey(User, related_name="entry_creators")
    creation_time = models.DateTimeField()


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






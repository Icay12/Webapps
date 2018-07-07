# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Data model for a todo-list item
class Item(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None)
    ip_addr = models.GenericIPAddressField()

    def __str__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'

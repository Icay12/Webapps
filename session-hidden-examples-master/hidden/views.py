# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def hidden_demo(request):
    context = {}

    if not 'first' in request.POST:
        return render(request, 'hidden/get-first.html', context)

    context['first'] = request.POST['first']

    if not 'last' in request.POST:
        return render(request, 'hidden/get-last.html', context)

    context['last'] = request.POST['last']

    if not 'what' in request.POST:
        return render(request, 'hidden/get-what.html', context)

    context['what'] = request.POST['what']

    return render(request, 'hidden/finish.html', context)

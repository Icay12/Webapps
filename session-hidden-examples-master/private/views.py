# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def home(request):
    if not 'name' in request.session:
        return render(request, 'private/name.html', {})

    context = {'name':request.session['name'], 'items':request.session['list']}
    return render(request, 'private/index.html', context)

def provide_name(request):
    errors = []  # A list to record messages for any errors we encounter.

    # Adds the new item to the list if the request parameter is present
    if not 'name' in request.POST or not request.POST['name']:
        errors.append('You must provide a name.')
        return render(request, 'private/name.html', {'errors':errors})

    request.session['name'] = request.POST['name']
    request.session['list'] = []

    context = {}
    context['name'] = request.session['name']
    context['items'] = request.session['list']
    context['errors'] = errors
    return render(request, 'private/index.html', context)

def add_item(request):
    errors = []  # A list to record messages for any errors we encounter.

    if not 'name' in request.session:
        return render(request, 'private/name.html', {})

    list = request.session['list']

    # Adds the new item to the list if the request parameter is present
    if not 'item' in request.POST or not request.POST['item']:
        errors.append('You must provide an item to add.')
    else:
        list.append(request.POST['item'])
        request.session.modified = True

    context = {}
    context['name'] = request.session['name']
    context['items'] = request.session['list']
    context['errors'] = errors

    return render(request, 'private/index.html', context)

def delete_item(request):
    errors = []

    if not 'name' in request.session:
        return render(request, 'private/name.html', {})

    list = request.session['list']

    if not 'item' in request.POST:
        errors.append('Missing parameter: item')
    else:
        item = request.POST['item']
        try:
            list.remove(item)
            request.session.modified = True
        except ValueError:
            errors.append('This item is not on the list: ' + item)

    context = {}
    context['name'] = request.session['name']
    context['items'] = request.session['list']
    context['errors'] = errors
    return render(request, 'private/index.html', context)

def delete_all(request):
    if not 'name' in request.session:
        return render(request, 'private/name.html', {})

    request.session['list'] = []

    context = {}
    context['name'] = request.session['name']
    context['items'] = request.session['list']
    return render(request, 'private/index.html', context)

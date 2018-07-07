from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from channels import Group

# Imports the Item class
from ws_todolist.models import *


@ensure_csrf_cookie
def home(request):
    return render(request, 'ws_todolist/index.html', {})

def add_item(request):
    if request.method != 'POST':
        raise Http404

    if not 'item' in request.POST or not request.POST['item']:
        message = 'You must enter an item to add.'
        json_error = '{ "error": "'+message+'" }'
        return HttpResponse(json_error, content_type='application/json')

    new_item = Item(text=request.POST['item'], ip_addr=request.META['REMOTE_ADDR'])
    new_item.save()


    Group('todolist').send({
        'text': serializers.serialize('json', Item.objects.all()),
    })

    message_text = 'Added Item(id={id})'.format(id=new_item.id)
    json_message = '{ "message": "' + message_text + '" }'
    return HttpResponse(json_message, content_type='application/json')

    
def delete_item(request, item_id):
    if request.method != 'POST':
        raise Http404

    item = get_object_or_404(Item, id=item_id)
    item.delete()


    Group('todolist').send({
        'text': serializers.serialize('json', Item.objects.all()),
    })

    message_text = 'Deleted Item(id={id})'.format(id=item_id)
    json_message = '{ "message": "' + message_text + '" }'
    return HttpResponse(json_message, content_type='application/json')

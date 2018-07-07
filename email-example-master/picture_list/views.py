from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

# Imports the Item class
from picture_list.models import *
from picture_list.forms  import *

from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    context = {}
    context['items'] = Item.objects.all()
    context['form']  = ItemForm()
    return render(request, 'picture_list/index.html', context)


@login_required
def add_item(request):
    context = {}

    new_item = Item(ip_addr=request.META['REMOTE_ADDR'])
    form = ItemForm(request.POST, request.FILES, instance=new_item)
    if not form.is_valid():
        context['form'] = form
    else:
        # Must copy content_type into a new model field because the model
        # FileField will not store this in the database.  (The uploaded file
        # is actually a different object than what's return from a DB read.)
        new_item.content_type = form.cleaned_data['picture'].content_type
        form.save()
        context['message'] = 'Item #{0} saved.'.format(new_item.id)
        context['form'] = ItemForm()

    context['items'] = Item.objects.all()
    return render(request, 'picture_list/index.html', context)

@login_required
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)

    context = {}

    if request.method != 'POST':
        context['message'] = 'Deletes must be done using the POST method'
    else:
        item = Item.objects.get(id=id)
        item.picture.delete()
        item.delete()
        context['message'] = 'Item deleted.'

    context['items'] = Item.objects.all()
    context['form']  = ItemForm()
    return render(request, 'picture_list/index.html', context)

@login_required
def get_photo(request, id):
    item = get_object_or_404(Item, id=id)

    # Probably don't need this check as form validation requires a picture be uploaded.
    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=item.content_type)

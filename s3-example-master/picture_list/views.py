from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

# Imports the Item class
from picture_list.models import *
from picture_list.forms  import *
from picture_list.s3 import s3_upload, s3_delete



def home(request):
    context = {}
    context['items'] = Item.objects.all()
    context['form']  = ItemForm()
    return render(request, 'picture_list/index.html', context)


def add_item(request):
    context = {}

    new_item = Item(ip_addr=request.META['REMOTE_ADDR'])
    form = ItemForm(request.POST, request.FILES, instance=new_item)
    if not form.is_valid():
        context['form'] = form

    else:
        # Save the new record (note: this sets value for entry.id)
        form.save()

        url = s3_upload(form.cleaned_data['picture'], new_item.id)
        new_item.picture_url = url
        new_item.save()

        context['message'] = 'Item #{0} saved.'.format(new_item.id)
        context['form'] = ItemForm()

    context['items'] = Item.objects.all()
    return render(request, 'picture_list/index.html', context)

# Action for the shared-todo-list/delete-item route.
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)

    context = {}

    if request.method != 'POST':
        context['message'] = 'Deletes must be done using the POST method'
    else:
        item.delete()
        s3_delete(id)
        context['message'] = 'Item deleted.'

    context['items'] = Item.objects.all()
    context['form']  = ItemForm()
    return render(request, 'picture_list/index.html', context)

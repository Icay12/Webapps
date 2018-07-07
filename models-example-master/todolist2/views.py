from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# Imports the Item class
from todolist2.models import *


# Action for the default /todolist2/ route.
@login_required
def home(request):
    # Gets a list of all the items in the todo-list database.
    all_items = Item.objects.all()

    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
    return render(request, 'todolist2/index.html', {'items': all_items})


# Action for the /todolist2/add-item route.
@login_required
def add_item(request):
    errors = []  # A list to record messages for any errors we encounter.

    # Adds the new item to the database if the request parameter is present
    if 'item' not in request.POST or not request.POST['item']:
        errors.append('You must enter an item to add.')
    else:
        new_item = Item(text=request.POST['item'],
                        user=request.user,
                        ip_addr=request.META['REMOTE_ADDR'])
        new_item.save()

    # Sets up data needed to generate the view, and generates the view
    items = Item.objects.all()
    context = {'items': items, 'errors': errors}
    return render(request, 'todolist2/index.html', context)


# Action for the /todolist2/delete-item route.
@login_required
def delete_item(request, item_id):
    errors = []

    if request.method != 'POST':
        errors.append('Deletes must be done using the POST method')
    else:
        # Deletes the item if present in the todo-list database.
        try:
            item_to_delete = Item.objects.get(id=item_id)
            item_to_delete.delete()
        except ObjectDoesNotExist:
            errors.append('The item did not exist in the To Do List.')

    items = Item.objects.all()
    context = {'items': items, 'errors': errors}
    return render(request, 'todolist2/index.html', context)

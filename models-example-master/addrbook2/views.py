from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone

from addrbook2.models import Entry
from addrbook2.forms import CreateForm, EditForm

import time # for adding sleep calls to demonstrate concurrency issues

@login_required
def search(request):
    if not 'last' in request.GET:
        return render(request, 'addrbook2/search.html', {})

    last = request.GET['last']
    objects = Entry.objects.filter(last_name__istartswith=last)

    if objects.count() == 0:
        message = 'No entries with last name = "{0}"'.format(last)
        return render(request, 'addrbook2/search.html', {'message': message})

    if objects.count() > 1:
        context = { 'entries': objects.order_by('last_name', 'first_name') }
        return render(request, 'addrbook2/list.html', context)

    entry = objects.all()[0]
    form = EditForm(instance=entry)
    context = { 'entry': entry, 'form': form }
    return render(request, 'addrbook2/edit.html', context)

@login_required
def create(request):
    if request.method == 'GET':
        context = { 'form': CreateForm() }
        return render(request, 'addrbook2/create.html', context)

    entry = Entry(created_by=request.user, creation_time=timezone.now(),
                  updated_by=request.user, update_time=timezone.now())
    create_form = CreateForm(request.POST, instance=entry)
    if not create_form.is_valid():
        context = { 'form': create_form }
        return render(request, 'addrbook2/create.html', context)
   
    # Save the new record
    create_form.save()

    message = 'Entry created'
    edit_form = EditForm(instance=entry)
    context = { 'message': message, 'entry': entry, 'form': edit_form }
    return render(request, 'addrbook2/edit.html', context)

@login_required
def delete(request, id):
    if request.method != 'POST':
        message = 'Invalid request.  POST method must be used.'
        return render(request, 'addrbook2/search.html', { 'message': message })

    entry = get_object_or_404(Entry, id=id)
    entry.delete()
    message = 'Entry for {0}, {1} has been deleted.'.format(entry.last_name, entry.first_name)
    return render(request, 'addrbook2/search.html', { 'message': message })

@login_required
@transaction.atomic
def edit(request, id):
    try:
        if request.method == 'GET':
            entry = Entry.objects.get(id=id)
            form = EditForm(instance=entry)
            context = { 'entry': entry, 'form': form }
            return render(request, 'addrbook2/edit.html', context)
    
        entry = Entry.objects.select_for_update().get(id=id)
        db_update_time = entry.update_time  # Copy timestamp to check after form is bound
        form = EditForm(request.POST, instance=entry)
        if not form.is_valid():
            context = { 'entry': entry, 'form': form }
            return render(request, 'addrbook2/edit.html', context)

        # if update times do not match, someone else updated DB record while were editing
        if db_update_time != form.cleaned_data['update_time']:
            # refetch from DB and try again.
            entry = Entry.objects.get(id=id)
            form = EditForm(instance=entry)
            context = {
                'message': 'Another user has modified this record.  Re-enter your changes.',
                'entry':   entry,
                'form':    form,
            }
            return render(request, 'addrbook2/edit.html', context)

        # Set update info to current time and user, and save it!
        entry.update_time = timezone.now()
        entry.updated_by  = request.user
        form.save()

        # form = EditForm(instance=entry)
        context = {
            'message': 'Entry updated.',
            'entry':   entry,
            'form':    form,
        }
        return render(request, 'addrbook2/edit.html', context)
    except Entry.DoesNotExist:
        context = { 'message': 'Record with id={0} does not exist'.format(id) }
        return render(request, 'addrbook2/search.html', context)

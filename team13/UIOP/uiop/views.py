
from django.shortcuts import render, get_object_or_404

def home(request):
    context = {}
    return render(request, 'index.html', context)
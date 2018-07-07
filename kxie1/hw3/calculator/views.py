# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def home_page(request):
    context = {'display': 0, 'newValue': 0, 'preValue': 0, 'preOperation': '+', 'preButton': 1, 'errors': []}
    return render(request, 'calculator/calculator.html', context)


def cal(request):
    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
    context = {'display': 0}
    newValue = 0
    preValue = 0
    preOperation = '+'
    preButton = 1  # 1:digit 0:operation
    display = 0

    errors = []  # A list to record messages for any errors we encounter.

    if ('digit' not in request.POST) and ('operation' not in request.POST or not request.POST['operation']):
        errors.append('You must press the buttons!')
        newValue = 0
        preValue = 0
        preOperation = '+'
        preButton = 1  # 1:digit 0:operation
        display = 0

    if 'newValue' in request.POST:
        print "newValue"
        newValue = int(request.POST['newValue'])

    if 'preValue' in request.POST:
        print "preValue"
        preValue = int(request.POST['preValue'])

    if 'preOperation' in request.POST:
        print "preOperation"
        preOperation = request.POST['preOperation']

    if 'preButton' in request.POST:
        print "preButton"
        preButton = int(request.POST['preButton'])

    if 'digit' in request.POST:
        print "digit"
        number = int(request.POST['digit'])
        # print number
        if preOperation == '=':
            newValue = 0
            preValue = 0
            preOperation = '+'

        newValue = newValue * 10 + number
        preButton = 1
        display = newValue
        # context['display'] = newValue

    if 'operation' in request.POST:
        print "operation"
        operation = request.POST['operation']
        # print operation
        if preButton == 1:
            if preOperation == '+':
                preValue = preValue + newValue
            elif preOperation == '-':
                preValue = preValue - newValue
            elif preOperation == '*':
                preValue = preValue * newValue
            elif preOperation == '/':
                if newValue == 0:
                    preValue = 0
                    operation = '+'
                    errors.append("Can't divide by 0!")
                else:
                    preValue = preValue / newValue
            display = preValue
            # context['display'] = preValue
            newValue = 0

            if operation != '=':
                preButton = 0

        preOperation = operation



    context['newValue'] = newValue
    context['preValue'] = preValue
    context['preOperation'] = preOperation
    context['preButton'] = preButton
    context['display'] = display
    context['errors'] = errors
    return render(request, 'calculator/calculator.html', context)




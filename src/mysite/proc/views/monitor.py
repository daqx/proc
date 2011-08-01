# -*- coding: utf-8 -*-
'''
Created on 27.07.2011

@author: D_Unusov
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.contrib.auth.decorators import permission_required
from django.shortcuts import *
from mysite.proc.models import *
from mysite.proc.views.forms import *
#from mysite.proc.views.grids import *


@permission_required('proc.view_monitor')
def show(request):
    s_list = ActualState.objects.all()   
    return render(request,'monitor.html', {'s_list': s_list})


@permission_required('proc.view_monitor')
def journal(request, id_):
    s_list = JourSostAgent.objects.filter( agent__id = id_).order_by('-date')  
    return render(request,'journal.html', {'s_list': s_list})

'''
def grid_handler(request):
    # handles pagination, sorting and searching
    grid = ExampleGrid()
    return HttpResponse(grid.get_json(request), mimetype="application/json")

def grid_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = ExampleGrid()
    return HttpResponse(grid.get_config(), mimetype="application/json")
'''
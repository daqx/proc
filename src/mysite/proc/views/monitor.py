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


@permission_required('proc.view_monitor')
def show(request):
    s_list = ActualState.objects.all()   
    return render(request,'monitor.html', {'s_list': s_list})


@permission_required('proc.view_monitor')
def journal(request, id_):
    s_list = JourSostAgent.objects.filter( agent__id = id_).order_by('-date')  
    return render(request,'journal.html', {'s_list': s_list})



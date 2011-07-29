# -*- coding: utf-8 -*-
'''
Created on 29.07.2011

@author: D_Unusov
'''

from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.shortcuts import *
from mysite.proc.models import *
from mysite.proc.util.jqgrid import JqGrid


class ExampleGrid(JqGrid):
    model = JourSostAgent # could also be a queryset
    fields = ['id', 'name', 'desc'] # optional 
    url = reverse('grid_handler')
    caption = 'My First Grid' # optional
    colmodel_overrides = {
        'id': { 'editable': False, 'width':10 },
    }

# -*- coding: utf-8 -*-
'''
Created on 29.07.2011

@author: D_Unusov
'''


from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from mysite.proc.sys_model import *
from mysite.proc.util.jqgrid import JqGrid

formatBoolLink='formatBoolLink'


class ExampleGrid(JqGrid):
    model = JourSostAgent # could also be a queryset
    fields = ['id', 'agent__user__username', 'link','cash_count', 'cash_code__name','printer__name', 'terminal__name'] # optional 
    url = '/proc/examplegrid/' #reverse('grid_handler')
    caption = 'My First Grid' # optional
    colmodel_overrides = {
        'id': { 'label': ('№'), 'editable': False, 'width':10, 'formatter':'showlink', 'formatoptions':{'baseLinkUrl':'jur/'} },
        'agent__user__username': {'index':'agent__user__username', 'label': 'Агент','editable': False, 'width':20 },
        'link': { 'label': 'Канал','editable': False, 'width':10 , 'formatter':"extFormatBoolLink"},
    }


def grid_handler(request):
    # handles pagination, sorting and searching
    grid = ExampleGrid()
    request.session['test'] = 'test'  
    request.session.modified = True 
    #grid.model = ActualState
    return HttpResponse(grid.get_json(request), mimetype="application/json")

def grid_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = ExampleGrid()
    #grid.model = ActualState
    return HttpResponse(grid.get_config(), mimetype="application/json")
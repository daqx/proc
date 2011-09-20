# -*- coding: utf-8 -*-
'''
Created on 29.07.2011

@author: D_Unusov
'''


from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from mysite.proc.sys_model import *
from mysite.proc.util.jqgrid import JqGrid
from mysite.proc.models import *

formatBoolLink='formatBoolLink'


class JournalGrid(JqGrid):
    model = JourSostAgent # could also be a queryset
    
    fields = ['id', 'date','agent__id','agent__user__username', 'link','cash_count', 'cash_code__name','printer__name', 'terminal__name'] # optional 
    url = '/proc/examplegrid/' #reverse('grid_handler')
    caption = 'My First Grid' # optional
    colmodel_overrides = {
        'id': { 'label': ('№'), 'editable': False, 'width':10, 'formatter':'showlink', 'formatoptions':{'baseLinkUrl':'jur/'} },
        'agent__user__username': {'index':'agent__user__username', 'label': 'Агент','editable': False, 'width':20 },
        'link': { 'label': 'Канал','editable': False, 'width':10 , 'formatter':"extFormatBoolLink"},
    }
    
    def __init__(self, ag_id):        
        self.queryset = JourSostAgent.objects.filter(agent__id = ag_id).values('id', 'date','agent__id','agent__user__username', 'link','cash_count', 'cash_code__name','printer__name', 'terminal__name')
        


def journal_handler(request, id_):
    # handles pagination, sorting and searching
    grid = JournalGrid(id_)
    #request.session['test'] = 'test'  
    #request.session.modified = True 
    #grid.model = ActualState
    return HttpResponse(grid.get_json(request), mimetype="application/json")



class ActualStateGrid(JqGrid):
    model = ActualState # could also be a queryset
    fields = ['id', 'date','agent__id','agent__user__username', 'link','cash_count', 'cash_code__name','printer__name', 'terminal__name'] # optional 
    url = '/proc/examplegrid/' #reverse('grid_handler')
    caption = 'State Grid' # optional
    colmodel_overrides = {
        'id': { 'label': ('№'), 'editable': False, 'width':10, 'formatter':'showlink', 'formatoptions':{'baseLinkUrl':'jur/'} },
        'agent__user__username': {'index':'agent__user__username', 'label': 'Агент','editable': False, 'width':20 },
        'link': { 'label': 'Канал','editable': False, 'width':10 , 'formatter':"extFormatBoolLink"},
    }
    
    

def grid_handler(request):
    # handles pagination, sorting and searching
    grid = ActualStateGrid()
    #request.session['test'] = 'test'  
    #request.session.modified = True 
    #grid.model = ActualState
    return HttpResponse(grid.get_json(request), mimetype="application/json")

def grid_config(request):
    # build a config suitable to pass to jqgrid constructor   
    grid = JournalGrid()
    #grid.model = ActualState
    return HttpResponse(grid.get_config(), mimetype="application/json")

class PayGrid(JqGrid):
    model = Transaction # could also be a queryset    
    #fields = ['id', 'date','agent__id','agent__user__username', 'link','cash_count', 'cash_code__name','printer__name', 'terminal__name'] # optional 
    url = '/proc/examplegrid/' #reverse('grid_handler')
    caption = 'Pay' # optional
    
    
    def __init__(self, ag_id):        
        self.queryset = Transaction.objects.all().values('id', 'date','agent__id','agent__user__username', 'agent__dealer__user__username','summa','summa_pay', 'state__name')
        


def pay_handler(request, id_=0):
    
    grid = PayGrid(id_)    
    return HttpResponse(grid.get_json(request), mimetype="application/json")

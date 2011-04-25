# -*- coding: utf-8 -*-
'''
Created on 13.04.2011

@author: Admin
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import render_to_response
from mysite.proc.models import *
from mysite.proc.views.forms import *

''' ================================ PAY ========================'''
def pay_list(request):
    s_list = Transaction.objects.all()
    return render_to_response('pay.html', {'s_list': s_list})

def pay_form(request,id_):
    if request.method=='POST':
        a = Transaction.objects.get(pk=id_)

        form=TransactionForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            a = form.save(commit = False)
            
            a.save()
            return HttpResponseRedirect('/proc/agent/')
        else:
            return render_to_response('agent_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        s = Agent.objects.get(id=id_)
        form=AgentForm(instance=s,initial={'username' : s.user.username ,})
        del_url="%s/delete" % id_
                
        return render_to_response('agent_form.html', {'form': form,'del_url': del_url},context_instance=RequestContext(request))

def pay_delete(request,id_):
        s = Transaction.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/pay')
    
def pay_form_add(request,id_=0):
    if request.method=='POST':
        form=TransactionForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)            
            
            d.save()
            return HttpResponseRedirect('/proc/pay/')
        else:
            return render_to_response('pay_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        form=TransactionForm()      
        return render_to_response('pay_form.html', {'form': form},context_instance=RequestContext(request))
          
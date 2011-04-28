# -*- coding: utf-8 -*-
'''
Created on 21.03.2011

@author: Admin
'''
from django.template import loader,Context,RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import request
from django.shortcuts import render_to_response
from mysite.proc.models import *
from mysite.proc.views.forms import *

''' ================================ DEALER ========================'''
def dealer(request):
    s_list = Dealer.objects.all()   
    return render_to_response('dealer.html', {'s_list': s_list})

def dealer_form(request,id_):
    if request.method=='POST':
        a = Dealer.objects.get(pk=id_)

        form=DealerEditForm(request.POST, instance=a)
        if form.is_valid():
            a = form.save(commit = False)
            u=User.objects.get(pk=a.user.id)
            u.username=form.cleaned_data["username"]
            u.save()
            a.save()
            return HttpResponseRedirect('/proc/dealer/')
        else:
            return render_to_response('dealer_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        s = Dealer.objects.get(id=id_)
        form=DealerEditForm(instance=s,initial={'username' : s.user.username ,})
        
        del_url="%s/delete" % id_
        
        return render_to_response('dealer_form.html', {'form': form,'del_url': del_url},context_instance=RequestContext(request))

def dealer_delete(request,id_):
        s = Dealer.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/dealer')

def dealer_form_add(request,id_=0):
    if request.method=='POST':
        form=DealerForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            u=User.objects.create_user(form.cleaned_data["username"], '', form.cleaned_data["password"])
            u.save()
            d.user = u
            d.save()
            return HttpResponseRedirect('/proc/dealer/')
        else:
            return render_to_response('dealer_form.html', {'form': form},context_instance=RequestContext(request))
    else:
        '''���������� ������ �������'''
        form=DealerForm(initial={'password':'', 'username' : ''})      
        return render_to_response('dealer_form.html', {'form': form},context_instance=RequestContext(request))
    
''' ================================ AGENT ========================'''

def agent(request):
    s_list = Agent.objects.all()    
    return render_to_response('agent.html', {'s_list': s_list})

def agent_form(request,id_):
    if request.method=='POST':
        a = Agent.objects.get(pk=id_)

        form=AgentEditForm(request.POST, instance=a)
        #form.type = ServiceType.objects.get(pk= request.POST['type'])
        if form.is_valid():
            a = form.save(commit = False)
            u=User.objects.get(pk=a.user.id)
            u.username=form.cleaned_data["username"]
            u.save()
            a.save()
            return HttpResponseRedirect('/proc/agent/')
        else:
            return render_to_response('agent_form.html', {'form': form},context_instance=RequestContext(request))
    else:        
        s = Agent.objects.get(id=id_)
        form=AgentEditForm(instance=s,initial={'username' : s.user.username ,})
        del_url="%s/delete" % id_
                
        return render_to_response('agent_form.html', {'form': form,'del_url': del_url},context_instance=RequestContext(request))

def agent_delete(request,id_):
        s = Agent.objects.get(id=id_)
        s.delete()
        return HttpResponseRedirect('/proc/agent')
    
def agent_form_add(request,id_=0):
    if request.method=='POST':
        form=AgentForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            u=User.objects.create_user(form.cleaned_data["username"], '', form.cleaned_data["password"])
            u.save()
            d.user = u
            d.save()
            return HttpResponseRedirect('/proc/agent/')
        else:
            return render_to_response('agent_form.html', {'form': form},context_instance=RequestContext(request))
    else:
        
        form=AgentForm(initial={'password':'', 'username' : ''})      
        return render_to_response('agent_form.html', {'form': form},context_instance=RequestContext(request))
       